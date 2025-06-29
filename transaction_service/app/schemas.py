from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class TxCreate(BaseModel):
    from_user: UUID
    to_user: UUID
    amount: Decimal
    currency: str = "USD"


class TxRead(BaseModel):
    id: UUID
    from_user: UUID
    to_user: UUID
    amount: Decimal
    currency: str
    status: str
