from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetFileOrFolderResponseLastModifyingUser(BaseModel):
    """
    Attributes:
        display_name (Optional[str]): Shows the display name of the user who last modified the file. Example: Dev User1.
        email_address (Optional[str]): Email address of the user who last modified the file. Example: devuser1@uipath-
                dev.com.
        kind (Optional[str]): The type of user who last modified the file. Example: drive#user.
        me (Optional[bool]): Shows if the last person to modify the file is you. Example: True.
        permission_id (Optional[str]): The permission ID of the user who last modified the file. Example:
                03464898141015738316.
        photo_link (Optional[str]): URL to the profile photo of the last user who modified the file. Example:
                https://lh3.googleusercontent.com/a/ACg8ocJA8OAiIs7P5QTkbRh8Kr3IaiAVH4Oc2TmLCaRg8w2gik8cTw=s64.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display_name: Optional[str] = Field(alias="displayName", default=None)
    email_address: Optional[str] = Field(alias="emailAddress", default=None)
    kind: Optional[str] = Field(alias="kind", default=None)
    me: Optional[bool] = Field(alias="me", default=None)
    permission_id: Optional[str] = Field(alias="permissionId", default=None)
    photo_link: Optional[str] = Field(alias="photoLink", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetFileOrFolderResponseLastModifyingUser"], src_dict: Dict[str, Any]
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
