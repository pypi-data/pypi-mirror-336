from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class SendMessageToUserRequestAttachmentsActionsConfirm(BaseModel):
    """
    Attributes:
        dismiss_text (Optional[str]):  Example: No.
        ok_text (Optional[str]):  Example: Yes.
        text (Optional[str]):  Example: Wouldn't you prefer a good game of chess?.
        title (Optional[str]):  Example: Are you sure?.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dismiss_text: Optional[str] = Field(alias="dismiss_text", default=None)
    ok_text: Optional[str] = Field(alias="ok_text", default=None)
    text: Optional[str] = Field(alias="text", default=None)
    title: Optional[str] = Field(alias="title", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["SendMessageToUserRequestAttachmentsActionsConfirm"],
        src_dict: Dict[str, Any],
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
