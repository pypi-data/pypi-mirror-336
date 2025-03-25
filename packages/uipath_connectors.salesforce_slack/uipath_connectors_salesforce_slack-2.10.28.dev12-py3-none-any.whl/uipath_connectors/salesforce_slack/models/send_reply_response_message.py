from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.send_reply_response_message_attachments_array_item_ref import (
    SendReplyResponseMessageAttachmentsArrayItemRef,
)
from ..models.send_reply_response_message_blocks_array_item_ref import (
    SendReplyResponseMessageBlocksArrayItemRef,
)
from ..models.send_reply_response_message_bot_profile import (
    SendReplyResponseMessageBotProfile,
)
from ..models.send_reply_response_message_icons import SendReplyResponseMessageIcons
from ..models.send_reply_response_message_metadata import (
    SendReplyResponseMessageMetadata,
)
from ..models.send_reply_response_message_root import SendReplyResponseMessageRoot


class SendReplyResponseMessage(BaseModel):
    """
    Attributes:
        app_id (Optional[str]):  Example: A02CEJTE85R.
        attachments (Optional[list['SendReplyResponseMessageAttachmentsArrayItemRef']]):
        blocks (Optional[list['SendReplyResponseMessageBlocksArrayItemRef']]):
        bot_id (Optional[str]):  Example: B02CRAP7A23.
        bot_profile (Optional[SendReplyResponseMessageBotProfile]):
        icons (Optional[SendReplyResponseMessageIcons]):
        metadata (Optional[SendReplyResponseMessageMetadata]):
        root (Optional[SendReplyResponseMessageRoot]):
        subtype (Optional[str]):  Example: thread_broadcast.
        team (Optional[str]):  Example: TCU0VUNLT.
        text (Optional[str]):  Example: Would you like to play a game?.
        thread_ts (Optional[str]):  Example: 1675217357.904929.
        ts (Optional[str]):  Example: 1631092102.000400.
        type_ (Optional[str]):  Example: message.
        user (Optional[str]):  Example: UCUFVVCKS.
        username (Optional[str]):  Example: My Bot lalitha new.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: Optional[str] = Field(alias="app_id", default=None)
    attachments: Optional[list["SendReplyResponseMessageAttachmentsArrayItemRef"]] = (
        Field(alias="attachments", default=None)
    )
    blocks: Optional[list["SendReplyResponseMessageBlocksArrayItemRef"]] = Field(
        alias="blocks", default=None
    )
    bot_id: Optional[str] = Field(alias="bot_id", default=None)
    bot_profile: Optional["SendReplyResponseMessageBotProfile"] = Field(
        alias="bot_profile", default=None
    )
    icons: Optional["SendReplyResponseMessageIcons"] = Field(
        alias="icons", default=None
    )
    metadata: Optional["SendReplyResponseMessageMetadata"] = Field(
        alias="metadata", default=None
    )
    root: Optional["SendReplyResponseMessageRoot"] = Field(alias="root", default=None)
    subtype: Optional[str] = Field(alias="subtype", default=None)
    team: Optional[str] = Field(alias="team", default=None)
    text: Optional[str] = Field(alias="text", default=None)
    thread_ts: Optional[str] = Field(alias="thread_ts", default=None)
    ts: Optional[str] = Field(alias="ts", default=None)
    type_: Optional[str] = Field(alias="type", default=None)
    user: Optional[str] = Field(alias="user", default=None)
    username: Optional[str] = Field(alias="username", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["SendReplyResponseMessage"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
