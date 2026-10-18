"""Two-layer authentication for Saving Passwords:
1. Edge Origin Protection: Cloudflare Zero Trust (Access) RS256 JWT verification
   via ``Cf-Access-Jwt-Assertion`` header / ``CF_Authorization`` cookie.
2. Application Master Password: Stateless PBKDF2 + HMAC-SHA256 signed session
   cookies (``vault_session``) and Bearer tokens with brute-force rate limiting.
"""
import base64
import hashlib
import hmac
import json
import os
import secrets
import time
import urllib.request
from collections import defaultdict, deque
from functools import lru_cache
from typing import Deque, Dict, Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from dotenv import dotenv_values
from fastapi import HTTPException, Request, Response, status

from config import (
    AUTH_PASSWORD_ENV_VAR,
    CF_ACCESS_AUD_ENV_VAR,
    CF_ACCESS_TEAM_DOMAIN_ENV_VAR,
    LOGIN_MAX_ATTEMPTS,
    LOGIN_WINDOW_SECONDS,
    PRIVATE_KEY_ENV_FILE,
    PRIVATE_KEY_ENV_VAR,
    SESSION_COOKIE_NAME,
    SESSION_TTL_HOURS,
)

_PBKDF2_ITERATIONS = 200_000
_PBKDF2_SALT = b"saving-passwords-master-auth-v1"


def _read_env_setting(var_name: str) -> Optional[str]:
    val = os.environ.get(var_name)
    if not val and PRIVATE_KEY_ENV_FILE.exists():
        val = dotenv_values(PRIVATE_KEY_ENV_FILE).get(var_name)
    return val.strip() if val and val.strip() else None


def get_auth_password() -> Optional[str]:
    """Return the configured master password from environment or ~/.env."""
    return _read_env_setting(AUTH_PASSWORD_ENV_VAR)


def is_auth_configured() -> bool:
    """Return True if SAVING_PASSWORDS_AUTH_PASSWORD is set."""
    return get_auth_password() is not None


@lru_cache(maxsize=4)
def _pbkdf2_digest(secret: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256", secret.encode("utf-8"), _PBKDF2_SALT, _PBKDF2_ITERATIONS
    )


def verify_master_password(candidate: str) -> bool:
    """Verify candidate password against SAVING_PASSWORDS_AUTH_PASSWORD in constant time."""
    expected = get_auth_password()
    if expected is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Server authentication is not configured ({AUTH_PASSWORD_ENV_VAR} is missing).",
        )
    cand_dk = hashlib.pbkdf2_hmac(
        "sha256", candidate.encode("utf-8"), _PBKDF2_SALT, _PBKDF2_ITERATIONS
    )
    exp_dk = _pbkdf2_digest(expected)
    return secrets.compare_digest(cand_dk, exp_dk)


@lru_cache(maxsize=4)
def _derive_signing_key(auth_password: str, priv_key_hint: str) -> bytes:
    """Derive a 32-byte HMAC key bound to the current master password and RSA private key."""
    salt = hashlib.sha256(f"session-key:{priv_key_hint}".encode("utf-8")).digest()
    return hashlib.pbkdf2_hmac("sha256", auth_password.encode("utf-8"), salt, 100_000)


def _get_signing_key() -> Optional[bytes]:
    pwd = get_auth_password()
    if not pwd:
        return None
    priv = _read_env_setting(PRIVATE_KEY_ENV_VAR) or "default-salt"
    return _derive_signing_key(pwd, priv[:64])


def create_session_token(ttl_seconds: Optional[int] = None) -> tuple[str, int]:
    """Create a stateless HMAC-SHA256 signed session token: v1.<exp>.<nonce>.<sig>."""
    signing_key = _get_signing_key()
    if not signing_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Server authentication is not configured ({AUTH_PASSWORD_ENV_VAR} is missing).",
        )
    if ttl_seconds is None:
        ttl_seconds = int(SESSION_TTL_HOURS * 3600)
    exp = int(time.time()) + ttl_seconds
    nonce = secrets.token_hex(16)
    payload = f"v1.{exp}.{nonce}"
    sig = hmac.new(signing_key, payload.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}", exp


def verify_session_token(token: Optional[str]) -> bool:
    """Verify a stateless HMAC-SHA256 session token."""
    signing_key = _get_signing_key()
    if not signing_key or not token or not isinstance(token, str):
        return False
    parts = token.split(".")
    if len(parts) != 4 or parts[0] != "v1":
        return False
    _, exp_str, nonce, sig = parts
    try:
        exp = int(exp_str)
    except ValueError:
        return False
    if time.time() > exp:
        return False
    payload = f"v1.{exp}.{nonce}"
    expected_sig = hmac.new(
        signing_key, payload.encode("ascii"), hashlib.sha256
    ).hexdigest()
    return secrets.compare_digest(sig, expected_sig)


# ── In-Memory Sliding Window Brute-Force Rate Limiter ──────────────────────
_failed_attempts: Dict[str, Deque[float]] = defaultdict(deque)


def get_client_ip(request: Request) -> str:
    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip:
        return cf_ip.strip()
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(ip: str) -> None:
    now = time.monotonic()
    q = _failed_attempts[ip]
    while q and (now - q[0]) > LOGIN_WINDOW_SECONDS:
        q.popleft()
    if len(q) >= LOGIN_MAX_ATTEMPTS:
        retry_after = max(1, int(LOGIN_WINDOW_SECONDS - (now - q[0])))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many failed attempts. Try again in {retry_after}s.",
            headers={"Retry-After": str(retry_after)},
        )


def record_failed_attempt(ip: str) -> None:
    _failed_attempts[ip].append(time.monotonic())


def clear_failed_attempts(ip: str) -> None:
    _failed_attempts.pop(ip, None)


# ── Cookie Helpers ─────────────────────────────────────────────────────────
def is_https_request(request: Request) -> bool:
    if request.url.scheme == "https":
        return True
    proto = request.headers.get("x-forwarded-proto", "")
    return "https" in proto.lower()


def set_session_cookie(response: Response, request: Request, token: str) -> None:
    max_age = int(SESSION_TTL_HOURS * 3600)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        secure=is_https_request(request),
        path="/",
    )


def clear_session_cookie(response: Response, request: Request) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        path="/",
        httponly=True,
        samesite="lax",
        secure=is_https_request(request),
    )


# ── FastAPI Dependency for App Session ─────────────────────────────────────
def extract_token_from_request(request: Request) -> Optional[str]:
    cookie_token = request.cookies.get(SESSION_COOKIE_NAME)
    if cookie_token:
        return cookie_token
    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return None


def is_request_authenticated(request: Request) -> bool:
    token = extract_token_from_request(request)
    return verify_session_token(token)


async def require_auth(request: Request) -> None:
    if not is_request_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vault is locked. Please enter your master password.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── Cloudflare Access JWT Verification (Origin Bypass Protection) ──────────
_cf_jwks_cache: Dict[str, rsa.RSAPublicKey] = {}
_cf_jwks_last_fetch: float = 0.0
_CF_JWKS_TTL = 3600.0
_CF_JWKS_MIN_REFRESH_INTERVAL = 60.0


def _b64url_decode(data: str) -> bytes:
    rem = len(data) % 4
    if rem:
        data += "=" * (4 - rem)
    return base64.urlsafe_b64decode(data.encode("ascii"))


def get_cf_access_config() -> tuple[Optional[str], Optional[str]]:
    """Return (issuer_url, aud_tag) if Cloudflare Zero Trust verification is configured."""
    domain = _read_env_setting(CF_ACCESS_TEAM_DOMAIN_ENV_VAR)
    aud = _read_env_setting(CF_ACCESS_AUD_ENV_VAR)
    if not domain or not aud:
        return None, None
    domain = domain.removeprefix("https://").removeprefix("http://").rstrip("/")
    if not domain.endswith(".cloudflareaccess.com"):
        domain = f"{domain}.cloudflareaccess.com"
    return f"https://{domain}", aud


def _fetch_cf_public_keys(issuer: str, force: bool = False) -> Dict[str, rsa.RSAPublicKey]:
    global _cf_jwks_cache, _cf_jwks_last_fetch
    now = time.monotonic()
    if not force and _cf_jwks_cache and (now - _cf_jwks_last_fetch) < _CF_JWKS_TTL:
        return _cf_jwks_cache
    if force and (now - _cf_jwks_last_fetch) < _CF_JWKS_MIN_REFRESH_INTERVAL and _cf_jwks_cache:
        return _cf_jwks_cache

    certs_url = f"{issuer}/cdn-cgi/access/certs"
    req = urllib.request.Request(certs_url, headers={"User-Agent": "SavingPasswords-Vault/1.0"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    keys: Dict[str, rsa.RSAPublicKey] = {}
    for jwk in data.get("keys", []):
        if jwk.get("kty") == "RSA" and "n" in jwk and "e" in jwk and "kid" in jwk:
            n = int.from_bytes(_b64url_decode(jwk["n"]), "big")
            e = int.from_bytes(_b64url_decode(jwk["e"]), "big")
            keys[jwk["kid"]] = rsa.RSAPublicNumbers(e, n).public_key()

    if keys:
        _cf_jwks_cache = keys
        _cf_jwks_last_fetch = now
    return _cf_jwks_cache


def verify_cf_access_jwt(token: str, issuer: str, expected_aud: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT structure")
    header_b64, payload_b64, sig_b64 = parts
    header = json.loads(_b64url_decode(header_b64))
    if header.get("alg") != "RS256":
        raise ValueError("Unsupported JWT algorithm")
    kid = header.get("kid")
    if not kid:
        raise ValueError("Missing kid in JWT header")

    keys = _fetch_cf_public_keys(issuer, force=False)
    if kid not in keys:
        keys = _fetch_cf_public_keys(issuer, force=True)
    pub_key = keys.get(kid)
    if not pub_key:
        raise ValueError("Unknown Cloudflare signing key")

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = _b64url_decode(sig_b64)
    pub_key.verify(signature, signing_input, padding.PKCS1v15(), hashes.SHA256())

    claims = json.loads(_b64url_decode(payload_b64))
    now = time.time()
    if claims.get("exp", 0) < (now - 60):
        raise ValueError("Cloudflare Access token has expired")
    if claims.get("nbf", 0) > (now + 60):
        raise ValueError("Cloudflare Access token not yet valid")
    if claims.get("iss", "").rstrip("/") != issuer.rstrip("/"):
        raise ValueError("Invalid JWT issuer")

    aud = claims.get("aud")
    aud_list = [aud] if isinstance(aud, str) else (aud or [])
    if expected_aud not in aud_list:
        raise ValueError("Invalid JWT audience")

    return claims
