import strawberry
from typing import Optional

async def _grpc_create_tx(amount: float):
    return {"id": "tx123", "amount": amount, "status": "PENDING"}


@strawberry.type
class Transaction:
    id: str
    amount: float
    status: str


@strawberry.type
class TransactionQuery:
    @strawberry.field
    async def transaction(self, info, id: str) -> Optional[Transaction]:
        # Stub for demo purposes
        if id == "tx123":
            return Transaction(id="tx123", amount=99.9, status="PENDING")
        return None
