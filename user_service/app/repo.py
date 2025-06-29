from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserRepo:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get(self, uid: UUID):
        return (await self._db.scalars(select(User).where(User.id == uid))).first()

    async def list_all(self):
        return (await self._db.scalars(select(User))).all()

    async def create(self, obj: User):
        self._db.add(obj)
        return obj
