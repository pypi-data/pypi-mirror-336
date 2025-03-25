# SPDX-FileCopyrightText: 2025 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import json
import re
import typing

from fedora_messaging import message

from .base import JOURNAL_SCHEMA, SCHEMA_URL


IPA_JOURNAL_FIELDS = (
    "IPA_API_ACTOR",
    "IPA_API_COMMAND",
    "IPA_API_PARAMS",
    "IPA_API_RESULT",
)
IPA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        **JOURNAL_SCHEMA["properties"],
        **{field: {"type": "string"} for field in IPA_JOURNAL_FIELDS},
    },
    "required": [*JOURNAL_SCHEMA["required"], *IPA_JOURNAL_FIELDS],
}

REDACT_FIELDS = ("MESSAGE", "IPA_API_PARAMS")
REDACT_EXPRS = (re.compile(r", \"mail\": \[[^\]]*\]"),)


class IpaMessage(message.Message):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by IPA.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in REDACT_FIELDS:
            for expr in REDACT_EXPRS:
                self.body[field] = expr.sub("", self.body[field])

    @property
    def _params(self):
        return json.loads(self.body["IPA_API_PARAMS"])

    @property
    def app_name(self):
        return "IPA"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/ipa.png"

    @property
    def agent_name(self):
        """The username of the user who initiated the action that generated this message."""
        return self.body["IPA_API_ACTOR"].partition("@")[0]

    @property
    def result(self):
        return self.body["IPA_API_RESULT"]


class IpaUserAddV1(IpaMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by IPA when a new user is created.
    """

    topic = "ipa.user_add.v1"
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when a new user is created",
        **IPA_SCHEMA,
    }

    @property
    def user_name(self):
        """The user that was created."""
        return self._params["uid"]

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return f"A new user has been created: {self.user_name}\nBy: {self.agent_name}\n"

    @property
    def summary(self):
        """Return a summary of the message."""
        return f'{self.agent_name} created user "{self.user_name}"'

    @property
    def usernames(self):
        return [self.user_name, self.agent_name]


class IpaGroupMemberMessage(IpaMessage):
    """
    A base class that defines a message schema for messages
    published by IPA when new users are added or removed from a group.
    """

    @property
    def user_names(self):
        """The users that were added or removed (list[str])."""
        return self._params["user"]

    @property
    def group(self):
        """The group that the users were added to or removed from."""
        return self._params["cn"]

    @property
    def usernames(self):
        return [self.agent_name, *self.user_names]

    @property
    def groups(self):
        return [self.group]


class IpaGroupAddMemberV1(IpaGroupMemberMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by IPA when new users are added to a group.
    """

    topic = "ipa.group_add_member.v1"
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when new users are added to a group",
        **IPA_SCHEMA,
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        user_list = "\n- ".join(self.user_names)
        return (
            f"Group {self.group} has new users:\n- {user_list}\n\n" f"Added by: {self.agent_name}\n"
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        if len(self.user_names) > 1:
            return (
                f'The following users were added to group "{self.group}" by {self.agent_name}: '
                f"{', '.join(self.user_names)}"
            )
        else:
            return (
                f'User "{self.user_names[0]}" has been added to group "{self.group}" '
                f"by {self.agent_name}"
            )


class IpaGroupRemoveMemberV1(IpaGroupMemberMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by IPA when new users are removed from a group.
    """

    topic = "ipa.group_remove_member.v1"
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when new users are removed from a group",
        **IPA_SCHEMA,
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        user_list = "\n- ".join(self.user_names)
        return (
            f"The following users were removed from group {self.group}:"
            f"\n- {user_list}\n\n"
            f"Removed by: {self.agent_name}\n"
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        if len(self.user_names) > 1:
            return (
                f'The following users were removed from group "{self.group}" by {self.agent_name}: '
                f"{', '.join(self.user_names)}"
            )
        else:
            return (
                f'User "{self.user_names[0]}" has been removed from group "{self.group}" '
                f"by {self.agent_name}"
            )
