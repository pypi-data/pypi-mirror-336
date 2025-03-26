"""Usage data collecting and storing in external sources."""

import os
import uuid
from typing import Any, Dict, Optional

import analytics
import click
import yaml
from pydantic import BaseModel

from db_contrib_tool.config import SEGMENT_WRITE_KEY


def _get_username() -> str:
    """
    Get username from .evergreen.yml.

    :return: Username or empty string.
    """
    try:
        with open(os.path.expanduser(os.path.join("~", ".evergreen.yml")), "r") as fh:
            evg_yml_data = yaml.safe_load(fh)
    except FileNotFoundError:
        evg_yml_data = {}
    return evg_yml_data.get("user", "")


USERNAME = _get_username()
ANONYMOUS_ID = str(uuid.uuid4())
analytics.write_key = SEGMENT_WRITE_KEY


class CommandUsage(BaseModel):
    """
    Command usage information.

    * command: Name of subcommand being invoked.
    """

    command: Optional[str]


class CommandWithUsageTracking(click.Command):
    """Class to track click command usage."""

    def invoke(self, ctx: click.Context) -> Any:
        """
        Given a context, this invokes the attached callback (if it exists) in the right way.

        :param ctx: Invocation context for this command.
        :return: Invocation result.
        """
        ctx.ensure_object(CommandUsage)
        track_usage(
            event="Command Line Tool Invoked",
            properties={
                "command": ctx.obj.command,
                "parsed_arguments": ctx.params,
            },
        )
        return super().invoke(ctx)


def track_usage(event: str, properties: Dict[str, Any]) -> None:
    """
    Track event.

    :param event: use Title Case event names, e.g. `Event Name`
    :param properties: use snake_case property keys, e.g. `property_name`,
        and serializable to JSON values
    """
    # Function call does not result in an HTTP request, but is queued in memory instead.
    # Messages are flushed in batch in the background
    # https://segment.com/docs/connections/sources/catalog/libraries/server/python/#batching
    analytics.track(
        user_id="",
        event=event,
        properties=properties,
        context={
            "traits": {
                "username": USERNAME,
            },
        },
        anonymous_id=ANONYMOUS_ID,
    )
