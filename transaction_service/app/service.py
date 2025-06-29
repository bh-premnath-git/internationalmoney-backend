import uuid
from .repo import TxRepo
from .models import Transaction
from .schemas import TxCreate
from common import db_session, publish, cache


class TxService:
    @staticmethod
    async def create_tx(data: TxCreate):
        async with db_session() as db:
            repo = TxRepo(db)
            tx = Transaction(id=uuid.uuid4(), **data.model_dump())
            await repo.create(tx)
            # publish event to Kafka
            await publish("transactions.created", tx.__dict__)
            return tx.__dict__

    @staticmethod
    @cache(ttl=120)
    async def get_tx(tid):
        async with db_session() as db:
            repo = TxRepo(db)
            tx = await repo.get(tid)
            return tx.__dict__ if tx else None
