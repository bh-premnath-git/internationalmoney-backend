import strawberry
from typing import Optional

# Stubbed async call – replace with gRPC client
async def _grpc_get_user(user_id: str):
    return {"id": user_id, "name": f"User {user_id}"}


@strawberry.type
class User:
    id: str
    name: str


@strawberry.type
class UserQuery:
    @strawberry.field
    async def user(self, info, id: str) -> Optional[User]:
        data = await _grpc_get_user(id)
        return User(**data) if data else None
