from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_vendor_response_address_2_country import (
    CreateVendorResponseAddress2Country,
)


class CreateVendorResponseAddress2(BaseModel):
    """
    Attributes:
        addr1 (Optional[str]): The Address 2 addr 1 Example: bimili.
        addr2 (Optional[str]): The Address 2 addr 2 Example: Gajuvaka.
        city (Optional[str]): The Address 2 city Example: Vizag.
        country (Optional[CreateVendorResponseAddress2Country]): The Address 2 country Example: _unitedStates.
        default_billing (Optional[bool]): The Address 2 default billing Example: true.
        default_shipping (Optional[bool]): The Address 2 default shipping Example: false.
        state (Optional[str]): The Address 2 state Example: AP.
        zip_ (Optional[str]): The Address 2 zip Example: 503494.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    addr1: Optional[str] = Field(alias="addr1", default=None)
    addr2: Optional[str] = Field(alias="addr2", default=None)
    city: Optional[str] = Field(alias="city", default=None)
    country: Optional["CreateVendorResponseAddress2Country"] = Field(
        alias="country", default=None
    )
    default_billing: Optional[bool] = Field(alias="defaultBilling", default=None)
    default_shipping: Optional[bool] = Field(alias="defaultShipping", default=None)
    state: Optional[str] = Field(alias="state", default=None)
    zip_: Optional[str] = Field(alias="zip", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateVendorResponseAddress2"], src_dict: Dict[str, Any]):
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
