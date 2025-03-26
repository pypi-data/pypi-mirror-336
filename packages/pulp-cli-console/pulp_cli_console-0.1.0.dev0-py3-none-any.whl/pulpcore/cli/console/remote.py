import click
from pulp_glue.common.i18n import get_translation
from pulp_glue.console.context import PulpConsoleRemoteContext
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    common_remote_create_options,
    common_remote_update_options,
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_pulp_context,
    show_command,
    update_command,
)

translation = get_translation(__package__)
_ = translation.gettext


@click.group()
@click.option(
    "-t",
    "--type",
    "remote_type",
    type=click.Choice(["console"], case_sensitive=False),
    default="console",
)
@pass_pulp_context
@click.pass_context
def remote(ctx: click.Context, pulp_ctx: PulpCLIContext, remote_type: str) -> None:
    """Manage remotes for console content."""
    if remote_type == "console":
        ctx.obj = PulpConsoleRemoteContext(pulp_ctx)
    else:
        raise NotImplementedError()


remote.add_command(list_command(decorators=[label_select_option]))
remote.add_command(show_command(decorators=[href_option, name_option]))
remote.add_command(create_command(decorators=common_remote_create_options))
remote.add_command(
    update_command(decorators=[href_option, name_option] + common_remote_update_options)
)
remote.add_command(destroy_command(decorators=[href_option, name_option]))
remote.add_command(label_command())
