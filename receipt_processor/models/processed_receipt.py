from uuid import uuid4

from pydantic import BaseModel, Field

from .receipt import Receipt


class ProcessedReceipt(BaseModel):
    """Processed Receipt base class."""

    unique_id: str = Field(default_factory=lambda: str(uuid4()))
    hash_value: str
    points: int | None = None
    receipt: Receipt
