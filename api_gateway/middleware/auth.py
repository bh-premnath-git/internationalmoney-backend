"""
JWT + Casbin RBAC middleware.
"""
import os
from typing import Any, Dict

from fastapi import Request
from fastapi.responses import JSONResponse
from casbin import Enforcer
from jwt import PyJWKClient, decode as jwt_decode
import cachetools

from ..config import get_settings

settings = get_settings()
_jwk_client = PyJWKClient(str(settings.JWKS_URL))
_cache: Dict[str, Any] = cachetools.TTLCache(maxsize=32, ttl=3600)

enforcer = Enforcer(model_path="api_gateway/rbac/model.conf",
                    adapter="api_gateway/rbac/policy.csv")


async def auth_middleware(request: Request, call_next):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse({"detail": "Missing token"}, status_code=401)

    token = auth.split()[1]
    # Fetch / cache signing key
    kid = jwt_decode(token, options={"verify_signature": False})["kid"]
    key = _cache.get(kid) or _jwk_client.get_signing_key(kid).key
    _cache[kid] = key
    try:
        claims = jwt_decode(token, key, algorithms=["RS256"], audience="account")
    except Exception as exc:
        return JSONResponse({"detail": f"Auth error: {exc}"}, status_code=401)

    # RBAC enforcement
    role = claims.get("realm_access", {}).get("roles", ["user"])[0]
    obj = request.url.path.split("/")[1] or "*"
    act = request.method.lower()
    if not enforcer.enforce(role, "global", obj, act):
        return JSONResponse({"detail": "Forbidden"}, status_code=403)

    # Pass user on downstream
    request.state.user = claims
    return await call_next(request)
