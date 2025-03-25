from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_customer_response_subscriptions_list_subscriptions_subscription import (
    CreateCustomerResponseSubscriptionsListSubscriptionsSubscription,
)
import datetime


class CreateCustomerResponseSubscriptionsListSubscriptionsArrayItemRef(BaseModel):
    """
    Attributes:
        last_modified_date (Optional[datetime.datetime]): The Subscriptions list subscriptions last modified date
                Example: 2024-05-09T11:57:39+05:30.
        subscribed (Optional[bool]): The Subscriptions list subscriptions subscribed
        subscription (Optional[CreateCustomerResponseSubscriptionsListSubscriptionsSubscription]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    last_modified_date: Optional[datetime.datetime] = Field(
        alias="lastModifiedDate", default=None
    )
    subscribed: Optional[bool] = Field(alias="subscribed", default=None)
    subscription: Optional[
        "CreateCustomerResponseSubscriptionsListSubscriptionsSubscription"
    ] = Field(alias="subscription", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateCustomerResponseSubscriptionsListSubscriptionsArrayItemRef"],
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
