""" Resources for the simple_rest_client to work with chatwoot API.

P.S. I'm proud of this one.
"""
import functools
from dataclasses import fields
from types import MethodType
from simple_rest_client.resource import Resource, AsyncResource

import woot.actions as a
from woot.utils import update_signature, extract_path_params


class ActionMeta(type):
    def __new__(cls, name, bases, attrs, actions):
        attrs["default_actions"] = {v.name: v.default for v in fields(actions)}
        new_class = super().__new__(cls, name, bases, attrs)
        return new_class


class WootResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for action_name in self.actions.keys():
            self.update_action(action_name)

    def update_action(self, action_name):
        action_schema = self.actions[action_name].schema_
        url_params = extract_path_params(self.actions[action_name].url)
        if action_schema is not None:
            action_schema = action_schema.__dataclass_fields__
        else:
            action_schema = {}

        action_method = getattr(self, action_name)

        @update_signature(action_schema, action_name, url_params)
        def wrapped_action_method(self, *args, **kwargs):
            fields = action_schema.keys()
            body = {k: v for k, v in kwargs.items() if k in fields}
            params = {k: str(v) for k, v in kwargs.items() if k in url_params}
            kwargs = {
                k: v for k, v in kwargs.items() if k not in body and k not in params
            }
            return action_method(
                *args,
                body=body,
                params=None if not params else params,
                headers=None,
                action_name=action_name,
                **kwargs,
            )

        setattr(self, action_name, MethodType(wrapped_action_method, self))

    def __repr__(self):
        actions = self.actions
        resource_name = self.__class__.__name__ + " actions:"
        max_action_len = max([len(action) for action in self.actions.keys()])
        max_method_len = max([len(action.method) for action in self.actions.values()])
        max_url_len = max([len(action.url) for action in self.actions.values()])

        header = f"{resource_name}\n{'-' * (max_action_len + max_method_len + max_url_len + 7)}\n"
        actions_str = ""

        for action_name, action in actions.items():
            actions_str += (
                f"{action_name.capitalize()}:".ljust(max_action_len + 2)
                + f"{action.method}".ljust(max_method_len + 2)
                + f"{action.url}".ljust(max_url_len + 2)
            )
            if action.query:
                actions_str += f"\n{' ' * (max_action_len + max_method_len + 6)}Query parameters: {action.query.__annotations__}"
            if action.schema_:
                actions_str += f"\n{' ' * (max_action_len + max_method_len + 6)}Payload schema: {action.schema_.__annotations__}"
            actions_str += "\n\n"

        return header + actions_str


class AsyncWootResource(AsyncResource, WootResource):
    pass


class AccountResource(WootResource, metaclass=ActionMeta, actions=a.AccountActions):
    pass


class AccountUsersResource(
    WootResource, metaclass=ActionMeta, actions=a.AccountUsersActions
):
    pass


class AgentBotsResource(WootResource, metaclass=ActionMeta, actions=a.AgentBotsActions):
    pass


class UsersResource(WootResource, metaclass=ActionMeta, actions=a.UsersActions):
    pass


class AccountAgentBotResource(
    WootResource, metaclass=ActionMeta, actions=a.AccountAgentBotActions
):
    pass


class AgentsResource(WootResource, metaclass=ActionMeta, actions=a.AgentsActions):
    pass


class CannedResponsesResource(
    WootResource, metaclass=ActionMeta, actions=a.CannedResponsesActions
):
    pass


class ContactsResource(WootResource, metaclass=ActionMeta, actions=a.ContactsActions):
    pass


class ConversationAssignmentResource(
    WootResource, metaclass=ActionMeta, actions=a.ConversationAssignmentActions
):
    pass


class ConversationLabelsResource(
    WootResource, metaclass=ActionMeta, actions=a.ConversationLabelsActions
):
    pass


class ConversationsResource(
    WootResource, metaclass=ActionMeta, actions=a.ConversationsActions
):
    pass


class CustomAttributesResource(
    WootResource, metaclass=ActionMeta, actions=a.CustomAttributesActions
):
    pass


class CustomFiltersResource(
    WootResource, metaclass=ActionMeta, actions=a.CustomFiltersActions
):
    pass


class InboxResource(WootResource, metaclass=ActionMeta, actions=a.InboxActions):
    pass


class IntegrationsResource(
    WootResource, metaclass=ActionMeta, actions=a.IntegrationsActions
):
    pass


class MessagesResource(WootResource, metaclass=ActionMeta, actions=a.MessagesActions):
    pass


class ProfileResource(WootResource, metaclass=ActionMeta, actions=a.ProfileActions):
    pass


class ReportsResource(WootResource, metaclass=ActionMeta, actions=a.ReportsActions):
    pass


class TeamsResource(WootResource, metaclass=ActionMeta, actions=a.TeamsActions):
    pass


class WebhooksResource(WootResource, metaclass=ActionMeta, actions=a.WebhooksActions):
    pass


class AutomationRuleResource(
    WootResource, metaclass=ActionMeta, actions=a.AutomationRuleActions
):
    pass


# Async


class AsyncAccountResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.AccountActions
):
    pass


class AsyncAccountUsersResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.AccountUsersActions
):
    pass


class AsyncAgentBotsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.AgentBotsActions
):
    pass


class AsyncUsersResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.UsersActions
):
    pass


class AsyncAccountAgentBotResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.AccountAgentBotActions
):
    pass


class AsyncAgentsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.AgentsActions
):
    pass


class AsyncCannedResponsesResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.CannedResponsesActions
):
    pass


class AsyncContactsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.ContactsActions
):
    pass


class AsyncConversationAssignmentResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.ConversationAssignmentActions
):
    pass


class AsyncConversationLabelsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.ConversationLabelsActions
):
    pass


class AsyncConversationsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.ConversationsActions
):
    pass


class AsyncCustomAttributesResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.CustomAttributesActions
):
    pass


class AsyncCustomFiltersResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.CustomFiltersActions
):
    pass


class AsyncInboxResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.InboxActions
):
    pass


class AsyncIntegrationsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.IntegrationsActions
):
    pass


class AsyncMessagesResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.MessagesActions
):
    pass


class AsyncProfileResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.ProfileActions
):
    pass


class AsyncReportsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.ReportsActions
):
    pass


class AsyncTeamsResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.TeamsActions
):
    pass


class AsyncWebhooksResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.WebhooksActions
):
    pass


class AsyncAutomationRuleResource(
    AsyncWootResource, metaclass=ActionMeta, actions=a.AutomationRuleActions
):
    pass


_ALL_RESOURCES = [
    k
    for k, v in globals().items()
    if all(
        [
            "Resource" in k,
            isinstance(v, ActionMeta),
            not k.startswith("Async"),
            k not in ("Resource", "AsyncResource", "WootResource", "AsyncWootResource"),
        ]
    )
]

_ALL_ASYNC_RESOURCES = [
    k
    for k, v in globals().items()
    if all(
        [
            "Resource" in k,
            k.startswith("Async"),
            k not in ("Resource", "AsyncResource", "WootResource", "AsyncWootResource"),
        ]
    )
]
