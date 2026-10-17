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
