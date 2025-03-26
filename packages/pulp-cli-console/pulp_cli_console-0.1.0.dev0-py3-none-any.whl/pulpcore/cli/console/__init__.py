from typing import Any

import click
from pulp_glue.common.i18n import get_translation
from pulpcore.cli.common.generic import pulp_group

from pulpcore.cli.console.distribution import distribution
from pulpcore.cli.console.remote import remote
from pulpcore.cli.console.repository import repository

translation = get_translation(__package__)
_ = translation.gettext

__version__ = "0.1.0.dev"


@pulp_group("console")
def console_group() -> None:
    """Manage Console plugin."""
    pass


def mount(main: click.Group, **kwargs: Any) -> None:
    """Mount the console commands to the CLI."""
    console_group.add_command(distribution)
    console_group.add_command(remote)
    console_group.add_command(repository)
    main.add_command(console_group)
