from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.send_chat_message_request_mentions_mentioned import (
    SendChatMessageRequestMentionsMentioned,
)


class SendChatMessageRequestMentions(BaseModel):
    """
    Attributes:
        id (Optional[int]):
        mention_text (Optional[str]):  Example: Prakash Buthukuri.
        mentioned (Optional[SendChatMessageRequestMentionsMentioned]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: Optional[int] = Field(alias="id", default=None)
    mention_text: Optional[str] = Field(alias="mentionText", default=None)
    mentioned: Optional["SendChatMessageRequestMentionsMentioned"] = Field(
        alias="mentioned", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["SendChatMessageRequestMentions"], src_dict: Dict[str, Any]
    ):
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
