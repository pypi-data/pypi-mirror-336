from typing import Optional

import click
from pulp_glue.common.context import (
    PulpEntityContext,
    PulpRemoteContext,
    PulpRepositoryContext,
)
from pulp_glue.common.i18n import get_translation
from pulp_glue.console.context import (
    PulpConsoleRemoteContext,
    PulpConsoleRepositoryContext,
)
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_pulp_context,
    pass_repository_context,
    repository_href_option,
    repository_lookup_option,
    resource_option,
    retained_versions_option,
    show_command,
    update_command,
    version_command,
)
from pulpcore.cli.core.generic import task_command

translation = get_translation(__package__)
_ = translation.gettext

remote_option = resource_option(
    "--remote",
    default_plugin="console",
    default_type="console",
    context_table={"console:console": PulpConsoleRemoteContext},
    href_pattern=PulpRemoteContext.HREF_PATTERN,
    help=_("Remote used for syncing in the form '[[<plugin>:]<resource_type>:]<name>' or by href."),
)


@click.group()
@click.option(
    "-t",
    "--type",
    "repo_type",
    type=click.Choice(["console"], case_sensitive=False),
    default="console",
)
@pass_pulp_context
@click.pass_context
def repository(ctx: click.Context, pulp_ctx: PulpCLIContext, repo_type: str) -> None:
    """Manage repositories for console content."""
    if repo_type == "console":
        ctx.obj = PulpConsoleRepositoryContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option]
nested_lookup_options = [repository_href_option, repository_lookup_option]
update_options = [
    click.option("--description"),
    remote_option,
    retained_versions_option,
]
create_options = update_options + [click.option("--name", required=True)]

repository.add_command(list_command(decorators=[label_select_option]))
repository.add_command(show_command(decorators=lookup_options))
repository.add_command(create_command(decorators=create_options))
repository.add_command(update_command(decorators=lookup_options + update_options))
repository.add_command(destroy_command(decorators=lookup_options))
repository.add_command(task_command(decorators=nested_lookup_options))
repository.add_command(version_command(decorators=nested_lookup_options))
repository.add_command(label_command(decorators=nested_lookup_options))


@repository.command()
@name_option
@href_option
@click.option("--mirror/--no-mirror", default=None)
@remote_option
@pass_repository_context
def sync(
    repository_ctx: PulpRepositoryContext,
    mirror: Optional[bool],
    remote: Optional[PulpEntityContext],
) -> None:
    """Sync the repository with a remote."""
    repository_ctx.sync(body={"remote": remote, "mirror": mirror})


# Custom commands
