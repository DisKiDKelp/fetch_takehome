"""Receipt Item"""

from typing import Annotated, Any

from pydantic import BeforeValidator

from .base_schema import BaseSchema, total_int_parsing


class Item(BaseSchema):
    """Receipt item base class."""

    short_description: str

    # Store at cent level
    price: Annotated[int, BeforeValidator(total_int_parsing)]
