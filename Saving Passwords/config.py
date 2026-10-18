"""Application configuration for Saving Passwords.

Encryption model (asymmetric, RSA-OAEP + AES-GCM hybrid):
  * The PUBLIC key lives with the application (``public_key.pem`` next to this file).
    It is only able to *encrypt*, so it is safe to ship/commit it.
  * The PRIVATE key lives ONLY on your machine, in ``~/.env`` under
    ``SAVING_PASSWORDS_PRIVATE_KEY`` (base64-encoded DER, single line).
    It is required to *decrypt* the stored passwords.

Run ``python generate_keys.py`` once to create both keys.
"""
import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

# Public key (encrypt only) - part of the application config.
PUBLIC_KEY_PATH = Path(
    os.environ.get("SAVING_PASSWORDS_PUBLIC_KEY_PATH", APP_DIR / "public_key.pem")
)

# Private key (decrypt) - read from the env var, or from the .env file in your home dir.
PRIVATE_KEY_ENV_VAR = "SAVING_PASSWORDS_PRIVATE_KEY"
PRIVATE_KEY_ENV_FILE = Path(
    os.environ.get("SAVING_PASSWORDS_ENV_FILE", Path.home() / ".env")
)

# Marker prepended to every encrypted value inside the pickle file.
ENCRYPTED_PREFIX = "enc:v1:"

# RSA key size used by generate_keys.py
RSA_KEY_SIZE = 3072

# ── Google Drive Persistence Configuration ──────────────────────────────────
# Default File ID for Saved.pkl in Google Drive (can be overridden via GDRIVE_FILE_ID)
DEFAULT_GDRIVE_FILE_ID = "1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A"
GDRIVE_FILE_ID_ENV_VAR = "GDRIVE_FILE_ID"

# Service account JSON file path (Render mounts Secret Files at /etc/secrets/<filename>)
GDRIVE_SERVICE_ACCOUNT_FILE_ENV_VAR = "GDRIVE_SERVICE_ACCOUNT_FILE"
RENDER_SECRET_FILE_PATH = Path("/etc/secrets/gdrive-service-account.json")
LOCAL_SERVICE_ACCOUNT_PATH = Path.home() / ".config" / "saving-passwords" / "gdrive-service-account.json"

# Optional base64-encoded service account JSON (alternative to file path)
GDRIVE_SERVICE_ACCOUNT_B64_ENV_VAR = "GDRIVE_SERVICE_ACCOUNT_B64"

# ── Application Authentication & Cloudflare Access Configuration ────────────
# Master password for unlocking the web UI / API (read from env or ~/.env)
AUTH_PASSWORD_ENV_VAR = "SAVING_PASSWORDS_AUTH_PASSWORD"

# Session duration in hours (default: 24 hours)
SESSION_TTL_HOURS = float(os.environ.get("SAVING_PASSWORDS_SESSION_TTL_HOURS", "24"))

# Cookie name for the signed session token
SESSION_COOKIE_NAME = "vault_session"

# Brute-force rate-limiting for POST /api/auth/login
LOGIN_MAX_ATTEMPTS = int(os.environ.get("SAVING_PASSWORDS_LOGIN_MAX_ATTEMPTS", "5"))
LOGIN_WINDOW_SECONDS = int(os.environ.get("SAVING_PASSWORDS_LOGIN_WINDOW_SECONDS", "300"))

# Cloudflare Zero Trust (Access) Origin Verification
CF_ACCESS_TEAM_DOMAIN_ENV_VAR = "CF_ACCESS_TEAM_DOMAIN"
CF_ACCESS_AUD_ENV_VAR = "CF_ACCESS_AUD"

