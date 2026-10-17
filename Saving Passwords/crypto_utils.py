"""Encryption helpers for values persisted in Saved.pkl.

Each sensitive value is encrypted independently with a hybrid scheme:
  1. A fresh random 256-bit AES key encrypts the value with AES-GCM.
  2. That AES key is wrapped with the RSA public key (OAEP / SHA-256).
  3. Stored as: ENCRYPTED_PREFIX + base64(wrapped_key || nonce || ciphertext)

Only the private key (kept in ~/.env) can unwrap the AES key and decrypt.
Values without the prefix are treated as legacy plaintext and passed through
on read, so existing files are migrated transparently on the next save.
"""
import base64
import copy
import os
from functools import lru_cache

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import dotenv_values

from config import (
    ENCRYPTED_PREFIX,
    PRIVATE_KEY_ENV_FILE,
    PRIVATE_KEY_ENV_VAR,
    PUBLIC_KEY_PATH,
)

# Record fields that hold secrets and must be encrypted at rest.
ENCRYPTED_SCALAR_FIELDS = ("password",)
ENCRYPTED_LIST_FIELDS = ("password_history",)

_NONCE_SIZE = 12
_OAEP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)


class EncryptionKeyError(RuntimeError):
    """Raised when the public/private key cannot be loaded or do not match."""


@lru_cache(maxsize=1)
def load_public_key() -> rsa.RSAPublicKey:
    if not PUBLIC_KEY_PATH.exists():
        raise EncryptionKeyError(
            f"Public key not found at {PUBLIC_KEY_PATH}. Run `python generate_keys.py` first."
        )
    key = serialization.load_pem_public_key(PUBLIC_KEY_PATH.read_bytes())
    if not isinstance(key, rsa.RSAPublicKey):
        raise EncryptionKeyError(f"{PUBLIC_KEY_PATH} is not an RSA public key.")
    return key


@lru_cache(maxsize=1)
def load_private_key() -> rsa.RSAPrivateKey:
    raw = os.environ.get(PRIVATE_KEY_ENV_VAR)
    if not raw and PRIVATE_KEY_ENV_FILE.exists():
        raw = dotenv_values(PRIVATE_KEY_ENV_FILE).get(PRIVATE_KEY_ENV_VAR)
    if not raw:
        raise EncryptionKeyError(
            f"Private key not found. Set {PRIVATE_KEY_ENV_VAR} in {PRIVATE_KEY_ENV_FILE}."
        )

    try:
        key = serialization.load_der_private_key(base64.b64decode(raw), password=None)
    except Exception as exc:
        raise EncryptionKeyError(f"Could not parse {PRIVATE_KEY_ENV_VAR}: {exc}") from exc
    if not isinstance(key, rsa.RSAPrivateKey):
        raise EncryptionKeyError(f"{PRIVATE_KEY_ENV_VAR} is not an RSA private key.")

    if key.public_key().public_numbers() != load_public_key().public_numbers():
        raise EncryptionKeyError(
            f"The private key in {PRIVATE_KEY_ENV_FILE} does not match {PUBLIC_KEY_PATH}."
        )
    return key


def is_encrypted(value) -> bool:
    return isinstance(value, str) and value.startswith(ENCRYPTED_PREFIX)


def encrypt_value(value):
    """Encrypt a string with the public key. Non-strings / already encrypted are returned as-is."""
    if not isinstance(value, str) or is_encrypted(value):
        return value

    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(_NONCE_SIZE)
    ciphertext = AESGCM(aes_key).encrypt(nonce, value.encode("utf-8"), None)
    wrapped_key = load_public_key().encrypt(aes_key, _OAEP)

    return ENCRYPTED_PREFIX + base64.b64encode(wrapped_key + nonce + ciphertext).decode("ascii")


def decrypt_value(value):
    """Decrypt a value produced by encrypt_value. Legacy plaintext is returned as-is."""
    if not is_encrypted(value):
        return value

    blob = base64.b64decode(value[len(ENCRYPTED_PREFIX):])
    private_key = load_private_key()
    key_len = private_key.key_size // 8

    wrapped_key = blob[:key_len]
    nonce = blob[key_len:key_len + _NONCE_SIZE]
    ciphertext = blob[key_len + _NONCE_SIZE:]

    aes_key = private_key.decrypt(wrapped_key, _OAEP)
    return AESGCM(aes_key).decrypt(nonce, ciphertext, None).decode("utf-8")


def _transform_records(records: dict, fn) -> dict:
    out = copy.deepcopy(records)
    for record in out.values():
        if not isinstance(record, dict):
            continue
        for field in ENCRYPTED_SCALAR_FIELDS:
            if field in record:
                record[field] = fn(record[field])
        for field in ENCRYPTED_LIST_FIELDS:
            if isinstance(record.get(field), list):
                record[field] = [fn(v) for v in record[field]]
    return out


def encrypt_records(records: dict) -> dict:
    """Return a copy of the passwords dict with all secret fields encrypted."""
    return _transform_records(records, encrypt_value)


def decrypt_records(records: dict) -> dict:
    """Return a copy of the passwords dict with all secret fields decrypted."""
    return _transform_records(records, decrypt_value)


def count_plaintext_secrets(records: dict) -> int:
    """Number of secret values in `records` that are NOT encrypted."""
    count = 0
    for record in records.values():
        if not isinstance(record, dict):
            continue
        for field in ENCRYPTED_SCALAR_FIELDS:
            if isinstance(record.get(field), str) and not is_encrypted(record[field]):
                count += 1
        for field in ENCRYPTED_LIST_FIELDS:
            for v in record.get(field) or []:
                if isinstance(v, str) and not is_encrypted(v):
                    count += 1
    return count
