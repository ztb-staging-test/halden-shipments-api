"""API-key auth for partner and dashboard clients."""

import hmac
import os

from fastapi import Header, HTTPException, status


def _keys() -> dict[str, str]:
    # HALDEN_API_KEYS="dashboard:<key>,acme-3pl:<key>" injected from Secrets Manager at deploy.
    raw = os.environ.get("HALDEN_API_KEYS", "")
    return dict(pair.split(":", 1)[::-1] for pair in raw.split(",") if ":" in pair)


def require_client(x_api_key: str = Header(...)) -> str:
    """Returns the calling client's name, or 401."""
    for key, client in _keys().items():
        if hmac.compare_digest(key, x_api_key):
            return client
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid API key")
