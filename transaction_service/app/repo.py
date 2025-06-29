from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Transaction


class TxRepo:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get(self, tid: UUID):
        return (await self._db.scalars(select(Transaction).where(Transaction.id == tid))).first()

    async def list_for_user(self, uid: UUID):
        return (await self._db.scalars(select(Transaction).where(Transaction.from_user == uid))).all()

    async def create(self, obj: Transaction):
        self._db.add(obj)
        return obj
