from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_customer_request_address_1_country import (
    CreateCustomerRequestAddress1Country,
)


class CreateCustomerRequestAddress1(BaseModel):
    """
    Attributes:
        addr1 (Optional[str]): The Address 1 addr 1 Example: kukatpally.
        addr2 (Optional[str]): The Address 1 addr 2 Example: knr.
        city (Optional[str]): The Address 1 city Example: Hyd.
        country (Optional[CreateCustomerRequestAddress1Country]): The Address 1 country Example: _india.
        default_billing (Optional[bool]): The Address 1 default billing Example: false.
        default_shipping (Optional[bool]): The Address 1 default shipping Example: true.
        state (Optional[str]): The Address 1 state Example: telanagana.
        zip_ (Optional[str]): The Address 1 zip Example: 485885485.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    addr1: Optional[str] = Field(alias="addr1", default=None)
    addr2: Optional[str] = Field(alias="addr2", default=None)
    city: Optional[str] = Field(alias="city", default=None)
    country: Optional["CreateCustomerRequestAddress1Country"] = Field(
        alias="country", default=None
    )
    default_billing: Optional[bool] = Field(alias="defaultBilling", default=None)
    default_shipping: Optional[bool] = Field(alias="defaultShipping", default=None)
    state: Optional[str] = Field(alias="state", default=None)
    zip_: Optional[str] = Field(alias="zip", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateCustomerRequestAddress1"], src_dict: Dict[str, Any]):
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
