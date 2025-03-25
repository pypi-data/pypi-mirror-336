from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListSecurityAlertsPropertiesSupportingEvidenceSupportingEvidenceListArrayItemRef(
    BaseModel
):
    r"""
    Attributes:
        title (Optional[str]): The title of the evidence supporting the security alert. Example: Details of the login
                event performed by the principal user NT AUTHORITY\SYSTEM not seen in the last 60 days..
        type_ (Optional[str]): The type of supporting evidence related to the security alert. Example: tabularEvidences.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: Optional[str] = Field(alias="title", default=None)
    type_: Optional[str] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListSecurityAlertsPropertiesSupportingEvidenceSupportingEvidenceListArrayItemRef"
        ],
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
