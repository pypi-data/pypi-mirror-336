from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class GetRegistrationTokenForHostpoolResponseSystemData(BaseModel):
    """
    Attributes:
        created_at (Optional[datetime.datetime]): The date and time when the token was created. Example:
                2024-11-10T15:24:25.66Z.
        created_by (Optional[str]): Identifies the user or application that created the resource. Example:
                a331fe45-2138-4874-b387-93633a6d5548.
        created_by_type (Optional[str]): Indicates the type of entity that created the resource. Example: Application.
        last_modified_at (Optional[datetime.datetime]): The date and time when the record was last updated. Example:
                2024-11-12T09:00:03.55Z.
        last_modified_by (Optional[str]): The user or system that last modified the resource. Example:
                divijsingh02@gmail.com.
        last_modified_by_type (Optional[str]): The type of entity that last modified the resource. Example: User.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_at: Optional[datetime.datetime] = Field(alias="createdAt", default=None)
    created_by: Optional[str] = Field(alias="createdBy", default=None)
    created_by_type: Optional[str] = Field(alias="createdByType", default=None)
    last_modified_at: Optional[datetime.datetime] = Field(
        alias="lastModifiedAt", default=None
    )
    last_modified_by: Optional[str] = Field(alias="lastModifiedBy", default=None)
    last_modified_by_type: Optional[str] = Field(
        alias="lastModifiedByType", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetRegistrationTokenForHostpoolResponseSystemData"],
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
