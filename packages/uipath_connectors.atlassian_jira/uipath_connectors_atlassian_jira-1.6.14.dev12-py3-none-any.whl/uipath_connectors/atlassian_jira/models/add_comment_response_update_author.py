from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class AddCommentResponseUpdateAuthor(BaseModel):
    """
    Attributes:
        account_id (Optional[str]): The Update author account ID Example: 5b10a2844c20165700ede21g.
        active (Optional[bool]): The Update author active
        display_name (Optional[str]): The Update author display name Example: Mia Krystof.
        self_ (Optional[str]): The Update author self Example: https://your-
                domain.atlassian.net/rest/api/3/user?accountId=5b10a2844c20165700ede21g.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account_id: Optional[str] = Field(alias="accountId", default=None)
    active: Optional[bool] = Field(alias="active", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    self_: Optional[str] = Field(alias="self", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AddCommentResponseUpdateAuthor"], src_dict: Dict[str, Any]
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
