from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_customer_response_currency_list_currency_currency import (
    CreateCustomerResponseCurrencyListCurrencyCurrency,
)
from ..models.create_customer_response_currency_list_currency_symbol_placement import (
    CreateCustomerResponseCurrencyListCurrencySymbolPlacement,
)


class CreateCustomerResponseCurrencyListCurrencyArrayItemRef(BaseModel):
    """
    Attributes:
        balance (Optional[int]): The Currency list currency balance
        currency (Optional[CreateCustomerResponseCurrencyListCurrencyCurrency]):
        deposit_balance (Optional[int]): The Currency list currency deposit balance
        display_symbol (Optional[str]): The Currency list currency display symbol Example: $.
        overdue_balance (Optional[int]): The Currency list currency overdue balance
        override_currency_format (Optional[bool]): The Currency list currency override currency format
        symbol_placement (Optional[CreateCustomerResponseCurrencyListCurrencySymbolPlacement]):
        unbilled_orders (Optional[int]): The Currency list currency unbilled orders
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    balance: Optional[int] = Field(alias="balance", default=None)
    currency: Optional["CreateCustomerResponseCurrencyListCurrencyCurrency"] = Field(
        alias="currency", default=None
    )
    deposit_balance: Optional[int] = Field(alias="depositBalance", default=None)
    display_symbol: Optional[str] = Field(alias="displaySymbol", default=None)
    overdue_balance: Optional[int] = Field(alias="overdueBalance", default=None)
    override_currency_format: Optional[bool] = Field(
        alias="overrideCurrencyFormat", default=None
    )
    symbol_placement: Optional[
        "CreateCustomerResponseCurrencyListCurrencySymbolPlacement"
    ] = Field(alias="symbolPlacement", default=None)
    unbilled_orders: Optional[int] = Field(alias="unbilledOrders", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateCustomerResponseCurrencyListCurrencyArrayItemRef"],
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
