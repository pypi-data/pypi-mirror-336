import kubernetes_asyncio
from aiohttp.client_exceptions import ClientConnectorError
from dataclasses import dataclass
from enum import Enum
from kubernetes_utils.api import KubernetesAPIs
from kubernetes_utils.helpers import wait_for_state
from kubernetes_utils.ownership import OwnershipInformation
from log.log import LoggerMixin
from typing import Optional


@dataclass
class DynamicVolumeMount:
    persistent_volume_claim_name: str
    mount_path: str

    def name(self):
        return self.persistent_volume_claim_name


@dataclass
class ConfigMapMount:
    config_map_name: str
    mount_path: str

    def name(self):
        return self.config_map_name


@dataclass
class HostPathMount:
    mount_name: str
    host_path: str
    mount_path: str

    def name(self):
        return self.mount_name


@dataclass
class Container:
    name: str
    image_name: str
    args: Optional[list[str]] = None
    exposed_ports: Optional[list[int]] = None
    env: Optional[list[kubernetes_asyncio.client.V1EnvVar]] = None
    volumes: Optional[list[DynamicVolumeMount | ConfigMapMount | HostPathMount]
                     ] = None


class UpdateStrategy(Enum):
    """See:
    https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy
    """
    ROLLING_UPDATE = 'RollingUpdate'
    RECREATE = 'Recreate'


class AbstractDeployments:

    async def create_or_update(
        self,
        *,
        namespace: str,
        deployment_name: str,
        replicas: int,
        containers: list[Container],
        owner: Optional[OwnershipInformation] = None,
        service_account_name: Optional[str] = None,
        pod_labels: Optional[dict[str, str]] = None,
        update_strategy: Optional[UpdateStrategy] = None,
        termination_grace_period_seconds: Optional[int] = None,
    ):
        """Construct a deployment with the given number of replicas, where
        each pod runs the container with the given name.
        If a deployment with the given name already exists, replace it with the
        new one."""
        raise NotImplementedError

    async def list_for_name_prefix(
        self, namespace: str, name_prefix: str
    ) -> list[kubernetes_asyncio.client.V1Deployment]:
        """Get all deployments that start with the given name prefix."""
        raise NotImplementedError

    async def delete(self, namespace: str, name: str):
        """Delete the deployment with the given name from the given namespace."""
        raise NotImplementedError

    async def wait_for_started(
        self,
        namespace: str,
        name: str,
        seconds_between_api_calls: float = 0.2,
    ):
        """
        Block until all pods in deployment with the given `name` have started.
        This only works for first time roll-outs.
        """
        raise NotImplementedError

    async def wait_for_deleted(
        self,
        namespace: str,
        name: str,
        seconds_between_api_calls: float = 0.2,
    ):
        """
        Block until the deployment with the given `name` has been deleted.
        """
        raise NotImplementedError


class Deployments(LoggerMixin, AbstractDeployments):
    """An implementation of `AbstractDeployments` that uses the real
    Kubernetes API.
    """

    DEPLOYMENT_NAME_LABEL = 'reboot.dev/deployment-name'

    def __init__(self, apis: KubernetesAPIs):
        super().__init__()
        self._apis = apis

    async def create_or_update(
        self,
        *,
        namespace: str,
        deployment_name: str,
        replicas: int,
        containers: list[Container],
        owner: Optional[OwnershipInformation] = None,
        service_account_name: Optional[str] = None,
        pod_labels: Optional[dict[str, str]] = None,
        update_strategy: Optional[UpdateStrategy] = None,
        termination_grace_period_seconds: Optional[int] = None,
    ):
        pod_labels = pod_labels or {}
        # The deployment name is used as a label on the pods. If it isn't set
        # correctly the deployment will refuse to be created, so don't let users
        # accidentally override that label.
        if self.DEPLOYMENT_NAME_LABEL in pod_labels:
            raise ValueError(
                'Pod labels cannot contain the key '
                f'{self.DEPLOYMENT_NAME_LABEL} because it is used internally '
            )

        update_strategy = update_strategy or UpdateStrategy.ROLLING_UPDATE

        deployment_metadata = kubernetes_asyncio.client.V1ObjectMeta(
            namespace=namespace,
            name=deployment_name,
        )
        if owner is not None:
            # Add the owner information to the metadata in place.
            owner.add_to_metadata(deployment_metadata)

        selector = kubernetes_asyncio.client.V1LabelSelector(
            match_labels={self.DEPLOYMENT_NAME_LABEL: deployment_name}
        )

        pod_labels |= {self.DEPLOYMENT_NAME_LABEL: deployment_name}
        pod_metadata = kubernetes_asyncio.client.V1ObjectMeta(
            labels=pod_labels,
        )

        k8s_containers: list[kubernetes_asyncio.client.V1Container] = []
        # Key: volume name (== volume claim name, config map name, ...).
        k8s_volumes: dict[str, kubernetes_asyncio.client.V1Volume] = {}
        for container in containers:
            exposed_ports = container.exposed_ports or []
            env = container.env or []
            volumes = container.volumes or []
            args = container.args or []

            ports = [
                kubernetes_asyncio.client.V1ContainerPort(
                    container_port=exposed_port
                ) for exposed_port in exposed_ports
            ]

            k8s_containers.append(
                kubernetes_asyncio.client.V1Container(
                    name=container.name,
                    image=container.image_name,
                    args=args,
                    # On local k8s clusters (e.g. k3d), we don't want to `Always` pull
                    # images (they've been pre-loaded manually), but on non-local
                    # clusters (e.g. on one of the cloud providers) we need to pull
                    # images (they can't be pre-loaded).
                    image_pull_policy='IfNotPresent',
                    ports=ports,
                    env=env,
                    volume_mounts=[
                        kubernetes_asyncio.client.V1VolumeMount(
                            name=volume.name(), mount_path=volume.mount_path
                        ) for volume in volumes
                    ]
                )
            )

            for volume in volumes:
                if isinstance(volume, DynamicVolumeMount):
                    # It is safe to blindly add the volume to the dictionary
                    # keyed by name; if a prior container uses the same volume
                    # it is guaranteed to have the exact same configuration,
                    # because the only variable is that name.
                    k8s_volumes[volume.persistent_volume_claim_name] = (
                        kubernetes_asyncio.client.V1Volume(
                            # In Kubernetes the name of a volume in the Pod can be
                            # different than the name of the Persistent Volume Claim
                            # it's referring to, which are both unrelated to the name
                            # under which that volume is mounted into the filesystem.
                            # That functionality is unnecessary for our use case, so to
                            # reduce complexity we make the name of the Pod's volume and
                            # the name of the Persistent Volume Claim the same.
                            name=volume.persistent_volume_claim_name,
                            persistent_volume_claim=kubernetes_asyncio.client.
                            V1PersistentVolumeClaimVolumeSource(
                                claim_name=volume.persistent_volume_claim_name
                            )
                        )
                    )
                elif isinstance(volume, ConfigMapMount):
                    k8s_volumes[volume.config_map_name] = (
                        kubernetes_asyncio.client.V1Volume(
                            name=volume.config_map_name,
                            config_map=kubernetes_asyncio.client.
                            V1ConfigMapVolumeSource(
                                name=volume.config_map_name
                            )
                        )
                    )
                elif isinstance(volume, HostPathMount):
                    k8s_volumes[volume.mount_name] = (
                        kubernetes_asyncio.client.V1Volume(
                            name=volume.mount_name,
                            host_path=kubernetes_asyncio.client.
                            V1HostPathVolumeSource(path=volume.host_path)
                        )
                    )
                else:
                    raise ValueError(
                        f'Unsupported volume type: {type(volume)}'
                    )

        pod_spec = kubernetes_asyncio.client.V1PodSpec(
            containers=k8s_containers,
            service_account_name=service_account_name,
            volumes=list(k8s_volumes.values()),
            termination_grace_period_seconds=termination_grace_period_seconds,
        )
        template = kubernetes_asyncio.client.V1PodTemplateSpec(
            metadata=pod_metadata, spec=pod_spec
        )
        deployment_spec = kubernetes_asyncio.client.V1DeploymentSpec(
            selector=selector,
            template=template,
            replicas=replicas,
            strategy=kubernetes_asyncio.client.V1DeploymentStrategy(
                type=update_strategy.value
            ),
        )

        async def retryable_create_or_update_deployment():
            body = kubernetes_asyncio.client.V1Deployment(
                metadata=deployment_metadata,
                spec=deployment_spec,
            )
            try:
                await self._apis.apps.create_namespaced_deployment(
                    namespace, body
                )
            except kubernetes_asyncio.client.exceptions.ApiException as e:
                if e.reason == 'Conflict':
                    await self._apis.apps.replace_namespaced_deployment(
                        deployment_name, namespace, body
                    )
                else:
                    raise

        await self._apis.retry_api_call(retryable_create_or_update_deployment)

    async def list_for_name_prefix(
        self, namespace: str, name_prefix: str
    ) -> list[kubernetes_asyncio.client.V1Deployment]:

        async def retryable_get_deployments(
        ) -> list[kubernetes_asyncio.client.V1Pod]:
            deployment_list = await self._apis.apps.list_namespaced_deployment(
                namespace
            )
            return deployment_list.items

        deployment_list = await self._apis.retry_api_call(
            retryable_get_deployments
        )
        return [
            deployment for deployment in deployment_list
            if deployment.metadata.name.startswith(name_prefix)
        ]

    async def delete(self, namespace: str, name: str):

        async def retryable_delete_deployment():
            try:
                await self._apis.apps.delete_namespaced_deployment(
                    name, namespace
                )
            except kubernetes_asyncio.client.exceptions.ApiException as e:
                if e.status == 404:
                    # The object doesn't exist, so we don't need to delete it.
                    pass
                else:
                    raise e

        await self._apis.retry_api_call(retryable_delete_deployment)

    async def wait_for_started(
        self,
        namespace: str,
        name: str,
        seconds_between_api_calls: float = 0.2,
    ):

        # TODO: make this work for all rollouts. Not just first time rollouts.
        async def check_deployments() -> bool:
            deployments = await self._apis.apps.list_namespaced_deployment(
                namespace=namespace
            )

            for deployment in deployments.items:
                # A rollout is complete when the number of currently
                # available replicas matches the number of specified
                # replicas.
                # This is equivalent to:
                # `kubectl rollout status deployment.apps/[deployment_name]`
                if (
                    deployment.metadata.name == name and
                    deployment.spec.replicas
                    == deployment.status.available_replicas
                ):
                    return True
                # TODO: raise an error if we notice
                # item[deployment_name].TimeOutReason so we fail early.
            return False

        await wait_for_state(
            check_deployments,
            ClientConnectorError,
            seconds_between_api_calls=seconds_between_api_calls,
        )

    async def wait_for_deleted(
        self,
        namespace: str,
        name: str,
        seconds_between_api_calls: float = 0.2,
    ):

        async def check_deployments() -> bool:
            deployments = await self._apis.apps.list_namespaced_deployment(
                namespace=namespace
            )
            return name not in [
                deployment.metadata.name for deployment in deployments.items
            ]

        await wait_for_state(
            check_deployments,
            ClientConnectorError,
            seconds_between_api_calls=seconds_between_api_calls,
        )
