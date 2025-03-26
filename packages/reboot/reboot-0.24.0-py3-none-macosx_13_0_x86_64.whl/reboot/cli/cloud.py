import argparse
import base64
import json
import tempfile
import traceback
from pathlib import Path
from rbt.cloud.v1alpha1.application.application_rbt import (
    Application,
    ConcurrentModificationError,
    InvalidInputError,
    Status,
)
from rbt.cloud.v1alpha1.auth.auth_rbt import APIKey
from rbt.v1alpha1.errors_pb2 import (
    PermissionDenied,
    StateAlreadyConstructed,
    StateNotConstructed,
    Unauthenticated,
)
from reboot.aio.aborted import Aborted
from reboot.aio.external import ExternalContext
from reboot.aio.types import ApplicationId
from reboot.cli import terminal
from reboot.cli.commands import run_command
from reboot.cli.rc import ArgumentParser, SubcommandParser
from reboot.cloud.api_keys import (
    InvalidAPIKeyBearerToken,
    parse_api_key_bearer_token,
)
from reboot.naming import (
    QualifiedApplicationName,
    make_qualified_application_name_from_user_id_and_application_name,
)

DEFAULT_REBOOT_CLOUD_URL = "https://cloud.prod1.rbt.cloud:9991"

_API_KEY_FLAG = '--api-key'


def add_cloud_options(subcommand: SubcommandParser, *, api_key_required: bool):
    """Add flags common to all `rbt` commands that interact with the cloud."""
    # TODO: Consider moving these to flags on the `cloud` subcommand using #3845

    subcommand.add_argument(
        '--cloud-url',
        type=str,
        help="the URL of the Reboot cloud API",
        default=DEFAULT_REBOOT_CLOUD_URL,
        non_empty_string=True,
    )
    # TODO: This should probably be read from a file by default.
    subcommand.add_argument(
        _API_KEY_FLAG,
        type=str,
        help="the API key to use to connect to the Reboot Cloud API",
        default=None,
        required=api_key_required,
        non_empty_string=True,
    )


def _application_url(application_id: ApplicationId, cloud_url: str) -> str:
    """
    Given a cloud URL (e.g. `https://cloud.prod1.rbt.cloud:9991`), returns the
    url for the given application (e.g. `https://a12345.prod1.rbt.cloud:9991`).
    """
    if not (
        cloud_url.startswith("https://") or cloud_url.startswith("http://")
    ):
        terminal.fail(
            f"Cloud URL '{cloud_url}' must have 'https://' or 'http://'."
        )
    protocol, hostname_port = cloud_url.split("://", maxsplit=1)
    if not hostname_port.startswith("cloud."):
        terminal.fail(
            f"Cloud host '{hostname_port}' is missing expected 'cloud.' prefix"
        )
    cell_hostname_port = hostname_port.removeprefix("cloud.")
    return f"{protocol}://{application_id}.{cell_hostname_port}"


def cloud_external_context(args) -> ExternalContext:
    api_key = args.api_key
    if api_key is None:
        terminal.fail(
            f"The {_API_KEY_FLAG} flag must be set in order to "
            "access the Reboot Cloud."
        )
    return ExternalContext(
        name="reboot-cli",
        bearer_token=api_key,
        url=args.cloud_url,
    )


def register_cloud(parser: ArgumentParser):
    """Register the 'cloud' subcommand with the given parser."""

    def _add_common_flags(subcommand: SubcommandParser):
        """Adds flags common to every `rbt cloud` subcommand."""

        add_cloud_options(subcommand, api_key_required=True)

        subcommand.add_argument(
            '--name',
            type=str,
            required=True,
            help="name of the application",
            non_empty_string=True,
        )

    up_subcommand = parser.subcommand('cloud up')
    _add_common_flags(up_subcommand)
    up_subcommand.add_argument(
        '--dockerfile',
        type=Path,
        help='the Dockerfile to build this application from',
        default='./Dockerfile',
    )

    down_subcommand = parser.subcommand('cloud down')
    _add_common_flags(down_subcommand)

    logs_subcommand = parser.subcommand('cloud logs')
    _add_common_flags(logs_subcommand)
    logs_subcommand.add_argument(
        '--follow',
        type=bool,
        default=False,
        help='if true, follows the logs as they are produced',
    )


async def _user_id_from_api_key(api_key: str, cloud_url: str) -> str:
    try:
        api_key_id, api_key_secret = parse_api_key_bearer_token(token=api_key)
    except InvalidAPIKeyBearerToken:
        # Note that we do not log the API key contents; they are a secret, which
        # we don't want to output to a log file (if any).
        terminal.fail(
            "Invalid API key shape (expected: "
            "'XXXXXXXXXX-XXXXXXXXXXXXXXXXXXXX')"
        )

    context = ExternalContext(
        name="user-id-from-api-key",
        url=cloud_url,
        # TODO(rjh): once APIKey reads the bearer token for `Authenticate`, use
        #            that instead of passing `secret` in the proto below.
    )

    try:
        return (
            await APIKey.ref(api_key_id).Authenticate(
                context,
                secret=api_key_secret,
            )
        ).user_id
    except Aborted as aborted:
        match aborted.error:
            case StateNotConstructed(  # type: ignore[misc]
            ) | PermissionDenied(  # type: ignore[misc]
            ) | Unauthenticated():  # type: ignore[misc]
                # Note that we do not log the API key contents; they
                # are a secret, which we don't want to output to a log
                # file (if any).
                terminal.fail("Invalid API key")
            case _:
                terminal.fail(f"Unexpected error: {aborted}")


async def _maybe_create_application(
    qualified_application_name: QualifiedApplicationName,
    cloud_url: str,
    api_key: str,
) -> None:
    """
    Creates the Application with the given `qualified_application_name` if it
    doesn't exist yet.
    """
    # Use a separate context for `Create()`, since that call is allowed to fail
    # and will then leave its context unable to continue due to idempotency
    # uncertainty.
    context = ExternalContext(
        name="cloud-up-create-application",
        url=cloud_url,
        bearer_token=api_key,
    )
    try:
        await Application.Create(context, qualified_application_name)
    except Aborted as aborted:
        match aborted.error:
            case StateAlreadyConstructed():  # type: ignore[misc]
                # That's OK; we just want the application to exist!
                pass
            case _:
                # Unexpected error, propagate it.
                raise


async def _parse_common_cloud_args(
    args: argparse.Namespace
) -> tuple[str, str]:

    user_id = await _user_id_from_api_key(
        api_key=args.api_key,
        cloud_url=args.cloud_url,
    )

    qualified_application_name = make_qualified_application_name_from_user_id_and_application_name(
        user_id=user_id,
        application_name=args.name,
    )

    return user_id, qualified_application_name


async def cloud_up(args: argparse.Namespace) -> None:
    """Implementation of the 'cloud up' subcommand."""

    user_id, qualified_application_name = await _parse_common_cloud_args(args)

    context = ExternalContext(
        name="cloud-up",
        url=args.cloud_url,
        bearer_token=args.api_key,
    )

    try:
        terminal.info("[😇] checking permissions...", end=" ")
        await _maybe_create_application(
            qualified_application_name=qualified_application_name,
            cloud_url=args.cloud_url,
            api_key=args.api_key,
        )
        application = Application.ref(qualified_application_name)

        pushinfo_response = await application.PushInfo(context)
        terminal.info("✅")

        registry_endpoint = (
            pushinfo_response.registry_url
            # Regardless of whether the prefix is "https" or "http", we must
            # remove it; the Docker client will decide for itself whether it
            # believes the registry is "secure" or "insecure". We hope it
            # guesses right, otherwise the requests will fail.
            .removeprefix("https://").removeprefix("http://")
        )
        docker_tag = f"{registry_endpoint}/{pushinfo_response.repository}:{pushinfo_response.tag}"

        digest = await _docker_build_and_push(
            dockerfile=args.dockerfile,
            tag=docker_tag,
            registry_endpoint=registry_endpoint,
            registry_username=pushinfo_response.username,
            registry_password=pushinfo_response.password,
        )

        terminal.info("[🚀] deploying...", end=" ")
        up_response = await application.Up(context, digest=digest)
    except Aborted as aborted:
        if isinstance(aborted.error, InvalidInputError):
            terminal.fail("🛑 failed:\n"
                          f"  {aborted.error.reason}")
        elif isinstance(aborted.error, ConcurrentModificationError):
            terminal.fail(
                "🛑 failed:\n"
                "  The application is already being `up`ped or `down`ed. "
                "Please wait until that operation completes."
            )
        else:
            # Note that `PermissionDenied` shouldn't happen, since the
            # application we're attempting to `Up()` is by definition owned by
            # the user.
            print(f"🛑 unexpected error: {aborted}")
            traceback.print_exc()
            terminal.fail("Please report this bug to the maintainers")

        # This code is unreachable.
        raise

    async for status_response in application.reactively().RevisionStatus(
        context, revision_number=up_response.revision_number
    ):
        revision = status_response.revision
        if revision.status == Status.UPPING:
            # Keep waiting.
            continue
        if revision.status == Status.UP:
            terminal.info(
                f"✅\n"
                "\n"
                f"  '{args.name}' is available at: {_application_url(up_response.application_id, args.cloud_url)}"
                "\n"
            )
            break
        if revision.status == Status.FAILED:
            terminal.fail(
                "🛑 failed:\n"
                f"  {revision.failure_reason}\n"
                "\n"
                "Please correct the issue and try again."
            )
        if revision.status == Status.DOWNING or revision.status == Status.DOWN:
            terminal.fail(
                "🛑 failed:\n"
                "  The application is being `down`ed. Please wait until that "
                "operation completes."
            )

        # A revision that we `Up()`ed will never be in the `DOWNING` or `DOWN`
        # state. Those only appear for revisions created by calling `Down()`.
        raise ValueError(
            f"Application reached an unexpected status: '{revision.status}'. "
            "Please report this bug to the maintainers."
        )


async def cloud_down(args: argparse.Namespace) -> None:
    """Implementation of the 'cloud down' subcommand."""

    user_id, qualified_application_name = await _parse_common_cloud_args(args)

    context = ExternalContext(
        name="cloud-down",
        url=args.cloud_url,
        bearer_token=args.api_key,
    )

    try:
        await Application.ref(qualified_application_name).Down(context)
    except Aborted as aborted:
        match aborted.error:
            case StateNotConstructed():  # type: ignore[misc]
                terminal.fail(
                    f"User '{user_id}' does not have an application named "
                    f"'{args.name}'"
                )
            case _:
                # There are no other expected errors for
                # `Down()`. Most notably, `PermissionDenied` can't
                # happen, since the application we're attempting to
                # `Down()` is by definition owned by the user.
                terminal.fail(f"Unexpected error: {aborted}")

    terminal.info(
        f"Success. Your application '{args.name}' is being terminated."
    )

    # TODO(rjh): once the CLoud waits to resolve `down_response.down_task_id`
    #            until the application has terminated, await the completion of
    #            `down_response.down_task_id` here, and tell the user when their
    #            application has in fact terminated.


async def cloud_logs(args: argparse.Namespace) -> None:
    """Implementation of the 'cloud logs' subcommand"""

    user_id, qualified_application_name = await _parse_common_cloud_args(args)

    context = ExternalContext(
        name="cloud-logs",
        url=args.cloud_url,
        bearer_token=args.api_key,
    )

    try:
        async for response in Application.ref(qualified_application_name).Logs(
            context, follow=args.follow
        ):
            for record in response.records:
                print(record.text)

    except Aborted as aborted:
        match aborted.error:
            case StateNotConstructed():  # type: ignore[misc]
                terminal.fail(
                    f"User '{user_id}' does not have an application named "
                    f"'{args.name}'"
                )
            case _:
                # There are no other expected errors for `Logs()`. Most notably,
                # `PermissionDenied` can't happen, since the application we're
                # attempting to call `Logs()` on is by definition owned by the
                # user.
                terminal.fail(f"Unexpected error: {aborted}")


async def _docker_build_and_push(
    dockerfile: Path,
    tag: str,
    registry_endpoint: str,
    registry_username: str,
    registry_password: str,
) -> str:
    """
    Builds and pushes an image with the given `tag` from the `dockerfile`.

    Returns the digest of the pushed image.
    """
    assert dockerfile.is_absolute()
    if not dockerfile.exists() or not dockerfile.is_file():
        terminal.fail(f"🛑 Could not find Dockerfile '{dockerfile}'")

    dockerfile_pretty = str(dockerfile)
    try:
        dockerfile_pretty = str(dockerfile.relative_to(Path.cwd()))
        if not dockerfile_pretty.startswith("."):
            dockerfile_pretty = f"./{dockerfile_pretty}"
    except ValueError:
        # This means the Dockerfile is not in the current working directory.
        # That's OK, we'll simply use the absolute path.
        pass

    await run_command(
        command=[
            "docker",
            "buildx",
            "build",
            # Reboot Cloud runs on AMD64, so its images must be built for that
            # platform.
            "--platform",
            "linux/amd64",
            "--file",
            str(dockerfile),
            "--tag",
            tag,
            ".",
        ],
        cwd=str(dockerfile.parent),
        icon="🐳",
        command_name="build",
        explanation=f"building container from '{dockerfile_pretty}'",
        capture_output=False,
    )

    try:
        # The push step we do with config from a temporary directory, which
        # allows us to use a one-time Docker `config.json`. That avoids
        # permanently storing the user's credentials in their normal
        # `~/.docker/config.json`.
        with tempfile.TemporaryDirectory() as tempdir:
            # Create a temporary Docker configuration file.
            docker_config = Path(tempdir) / "config.json"
            docker_config.write_text(
                json.dumps(
                    {
                        "auths":
                            {
                                registry_endpoint:
                                    {
                                        "auth":
                                            base64.b64encode(
                                                f"{registry_username}:{registry_password}"
                                                .encode()
                                            ).decode(),
                                    }
                            }
                    }
                )
            )

            # Push the image with the temporary Docker configuration.
            await run_command(
                command=[
                    "docker",
                    "--config",
                    str(tempdir),
                    "push",
                    tag,
                ],
                icon="🚛",
                command_name="push",
                explanation="pushing container",
                capture_output=False,
            )

        # Obtain the image digest.
        digest = (
            await run_command(
                command=[
                    "docker",
                    "inspect",
                    "--format",
                    "{{index .RepoDigests 0}}",
                    tag,
                ],
                icon="👀",
                command_name="inspect",
                explanation="inspecting container",
                capture_output=True,
                only_show_if_verbose=True,
            )
        ).rsplit("@", 1)[-1]

        return digest

    finally:
        # Remove the tag from the local Docker daemon so that it doesn't pollute the
        # user's list of images.
        await run_command(
            command=[
                "docker",
                "image",
                "remove",
                tag,
            ],
            icon="🧹",
            command_name="cleanup",
            explanation="cleaning up",
            capture_output=False,
            only_show_if_verbose=True,
        )
