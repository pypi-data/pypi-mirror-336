import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from enum import Enum
from reboot.settings import (
    ENVVAR_NODEJS_CONSENSUS,
    ENVVAR_RBT_DEV,
    ENVVAR_RBT_PARTITIONS,
    ENVVAR_RBT_SERVE,
    ENVVAR_REBOOT_CLOUD_VERSION,
)
from typing import Optional


class RunEnvironment(Enum):
    """Known run environments."""
    RBT_DEV = 1
    RBT_SERVE = 2
    RBT_CLOUD = 3


class TypescriptEnvironment(Enum):
    """Known typescript run environments."""
    DOES_NOT_EXIST = 0
    NODEJS_CONSENSUS = 1


@dataclass(
    kw_only=True,
    frozen=True,
)
class RunSettings:
    run_environment: RunEnvironment
    typescript_environment: TypescriptEnvironment


class InvalidRunEnvironment(RuntimeError):
    """Exception for when run environment cannot be determined."""
    pass


def _detect_run_environment() -> RunEnvironment:
    """Internal helper to determine what run environment we are in."""
    # NOTE: ordering matters here as we may have multiple environment
    # variables set but some take precedence to others.
    if os.environ.get(ENVVAR_REBOOT_CLOUD_VERSION) is not None:
        # This environment variable is only set by the Cloud's controller, so we
        # must be on the Cloud. NOTE that it is NOT sufficient to look for
        # environment variables set by Kubernetes - it is possible to run `rbt
        # serve` on Kubernetes without being in the Cloud.
        return RunEnvironment.RBT_CLOUD
    elif os.environ.get(ENVVAR_RBT_DEV, 'false').lower() == 'true':
        return RunEnvironment.RBT_DEV
    elif os.environ.get(ENVVAR_RBT_SERVE, 'false').lower() == 'true':
        return RunEnvironment.RBT_SERVE

    raise InvalidRunEnvironment()


def _detect_typescript_environment() -> TypescriptEnvironment:
    """Internal helper to determine what typescript environment we are in."""
    if os.environ.get(ENVVAR_NODEJS_CONSENSUS, 'false').lower() == 'true':
        return TypescriptEnvironment.NODEJS_CONSENSUS

    return TypescriptEnvironment.DOES_NOT_EXIST


def _detect_run_settings() -> RunSettings:
    """Internal helper to determine what run environment we are in."""

    run_environment = _detect_run_environment()
    typescript_environment = _detect_typescript_environment()

    return RunSettings(
        run_environment=run_environment,
        typescript_environment=typescript_environment,
    )


def on_cloud() -> bool:
    """Helper for checking if we are running in a 'rbt cloud'
    cluster."""
    try:
        run_settings = _detect_run_settings()
        return run_settings.run_environment == RunEnvironment.RBT_CLOUD
    except InvalidRunEnvironment:
        return False


def running_rbt_dev() -> bool:
    """Helper for checking if we are running in a local development
    environment."""

    try:
        run_settings = _detect_run_settings()
        return run_settings.run_environment == RunEnvironment.RBT_DEV
    except InvalidRunEnvironment:
        return False


@asynccontextmanager
async def fake_rbt_dev_environment():
    """Temporarily sets the run environment to resemble a valid `rbt dev`"""

    previous_rbt_dev_value = os.environ.get(ENVVAR_RBT_DEV)
    previous_rbt_partitions_value = os.environ.get(ENVVAR_RBT_PARTITIONS)
    os.environ[ENVVAR_RBT_DEV] = 'true'
    os.environ[ENVVAR_RBT_PARTITIONS] = '1'

    try:
        yield
    finally:

        def reset(envvar_name: str, previous_value: Optional[str]):
            if previous_value is None:
                del os.environ[envvar_name]
            else:
                os.environ[envvar_name] = previous_value

        reset(ENVVAR_RBT_DEV, previous_rbt_dev_value)
        reset(ENVVAR_RBT_PARTITIONS, previous_rbt_partitions_value)
