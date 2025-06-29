import ssl
import httpx
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from tenacity import retry, wait_fixed, stop_after_attempt

from .middleware.auth import auth_middleware
from .middleware.rate_limit import limiter
from .metrics import init_metrics
from .load_balancer import get_next_service
from .graphql import graphql_app

TLS_CTX = ssl.create_default_context()

app = FastAPI(title="Money-Transfer API Gateway", version="1.0.0")
app.add_middleware("http", auth_middleware)
app.state.limiter = limiter
init_metrics(app)

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc):
    return {"detail": "Rate limit exceeded"}, 429


@retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
async def _proxy(method, url, headers, body):
    async with httpx.AsyncClient(verify=TLS_CTX) as client:
        return await client.request(method, url, headers=headers, content=body, timeout=5)


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@limiter.limit("60/minute")
async def gateway(full_path: str, request: Request):
    group = "user" if full_path.startswith("user") else "transaction"
    upstream = f"{get_next_service(group)}/{full_path}"
    resp = await _proxy(request.method, upstream, dict(request.headers), await request.body())
    return resp.content, resp.status_code, resp.headers.items()
