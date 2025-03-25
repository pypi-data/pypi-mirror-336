from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.update_vendor_response_currency_list_vendor_currency_currency import (
    UpdateVendorResponseCurrencyListVendorCurrencyCurrency,
)


class UpdateVendorResponseCurrencyListVendorCurrencyArrayItemRef(BaseModel):
    """
    Attributes:
        balance (Optional[int]): The Currency list vendor currency balance
        currency (Optional[UpdateVendorResponseCurrencyListVendorCurrencyCurrency]):
        unbilled_orders (Optional[int]): The Currency list vendor currency unbilled orders
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    balance: Optional[int] = Field(alias="balance", default=None)
    currency: Optional["UpdateVendorResponseCurrencyListVendorCurrencyCurrency"] = (
        Field(alias="currency", default=None)
    )
    unbilled_orders: Optional[int] = Field(alias="unbilledOrders", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["UpdateVendorResponseCurrencyListVendorCurrencyArrayItemRef"],
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
