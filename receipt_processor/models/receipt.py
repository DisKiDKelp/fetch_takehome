from datetime import date, datetime, time
from typing import Annotated, Any

from pydantic import BeforeValidator

from .base_schema import BaseSchema, total_int_parsing
from .item import Item


def validate_purchase_time(value: Any):

    return datetime.strptime(value, "%H:%M").time()


class Receipt(BaseSchema):
    items: list[Item]
    purchase_date: date
    purchase_time: Annotated[time, BeforeValidator(validate_purchase_time)]
    retailer: str
    total: Annotated[int, BeforeValidator(total_int_parsing)]
