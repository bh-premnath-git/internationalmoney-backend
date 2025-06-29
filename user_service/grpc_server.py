import asyncio
import grpc
from prometheus_client import Counter, Histogram, start_http_server
from proto import userprofile_pb2, userprofile_pb2_grpc
from common.events.kafka import close_events, init_events, publish
from .app.service import UserService

REQ = Counter("user_grpc_requests_total", "Requests", ["method"])
LAT = Histogram("user_grpc_latency_seconds", "Latency", ["method"])


class UserRPC(userprofile_pb2_grpc.UserServiceServicer):
    async def GetUser(self, request, context):
        REQ.labels("GetUser").inc()
        with LAT.labels("GetUser").time():
            data = await UserService.get_user(request.id)
            if not data:
                context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
            return userprofile_pb2.User(**data)

    async def ListUsers(self, request, context):
        REQ.labels("ListUsers").inc()
        with LAT.labels("ListUsers").time():
            # simple demo: not cached
            # (convert SQLAlchemy model dicts to proto objects)
            from uuid import UUID
            users = await UserService.list_users()  # implement list_users similarly
            return userprofile_pb2.UserList(
                users=[userprofile_pb2.User(**u) for u in users]
            )


async def serve():
    start_http_server(9100)  # Prometheus
    await init_events()  # Kafka producer
    server = grpc.aio.server()
    userprofile_pb2_grpc.add_UserServiceServicer_to_server(UserRPC(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    try:
        await server.wait_for_termination()
    finally:
        await close_events()


if __name__ == "__main__":
    asyncio.run(serve())
