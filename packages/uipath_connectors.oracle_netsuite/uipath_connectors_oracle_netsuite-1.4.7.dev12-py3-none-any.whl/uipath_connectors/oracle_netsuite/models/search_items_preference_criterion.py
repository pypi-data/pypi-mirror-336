from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.search_items_preference_criterion_value import (
    SearchItemsPreferenceCriterionValue,
)


class SearchItemsPreferenceCriterion(BaseModel):
    """
    Attributes:
        value (Optional[SearchItemsPreferenceCriterionValue]): Set the NAFTA criterion for this item. Available values
                are:_A_B_C_D_E_F
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    value: Optional["SearchItemsPreferenceCriterionValue"] = Field(
        alias="value", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["SearchItemsPreferenceCriterion"], src_dict: Dict[str, Any]
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
