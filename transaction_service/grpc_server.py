import asyncio
import grpc
from prometheus_client import Counter, Histogram, start_http_server
from proto import banktransaction_pb2, banktransaction_pb2_grpc
from common.events.kafka import close_events, init_events
from .app.service import TxService

REQ = Counter("tx_grpc_requests_total", "Requests", ["method"])
LAT = Histogram("tx_grpc_latency_seconds", "Latency", ["method"])


class TxRPC(banktransaction_pb2_grpc.TransactionServiceServicer):
    async def CreateTransaction(self, request, context):
        REQ.labels("CreateTransaction").inc()
        with LAT.labels("CreateTransaction").time():
            data = await TxService.create_tx(request)
            return banktransaction_pb2.Transaction(**data)

    async def GetTransaction(self, request, context):
        REQ.labels("GetTransaction").inc()
        with LAT.labels("GetTransaction").time():
            data = await TxService.get_tx(request.id)
            if not data:
                context.abort(grpc.StatusCode.NOT_FOUND, "Transaction not found")
            return banktransaction_pb2.Transaction(**data)

    async def ListTransactionsForUser(self, request, context):
        # Implement list-for-user if needed
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Not implemented")

    async def Ping(self, request, context):
        return banktransaction_pb2.Empty()


async def serve():
    start_http_server(9100)
    await init_events()
    server = grpc.aio.server()
    banktransaction_pb2_grpc.add_TransactionServiceServicer_to_server(TxRPC(), server)
    server.add_insecure_port("[::]:50052")
    await server.start()
    try:
        await server.wait_for_termination()
    finally:
        await close_events()


if __name__ == "__main__":
    asyncio.run(serve())
