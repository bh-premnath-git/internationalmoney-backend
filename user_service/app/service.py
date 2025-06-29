from uuid import UUID
from .repo import UserRepo
from .models import User
from .schemas import UserCreate
from common import db_session, cache


class UserService:
    @staticmethod
    @cache(ttl=120)
    async def get_user(uid: UUID):
        async with db_session() as db:
            repo = UserRepo(db)
            user = await repo.get(uid)
            return user.__dict__ if user else None

    @staticmethod
    async def create(data: UserCreate):
        async with db_session() as db:
            repo = UserRepo(db)
            user = User(**data.model_dump())
            await repo.create(user)
            return user.__dict__
