"""Generate the RSA key pair used to encrypt Saved.pkl.

  * Public key  -> public_key.pem (next to the app; safe to commit)
  * Private key -> ~/.env as SAVING_PASSWORDS_PRIVATE_KEY (base64 DER, chmod 600)

Usage:
    python generate_keys.py            # refuses to overwrite existing keys
    python generate_keys.py --force    # replace keys (only if Saved.pkl has no encrypted data)
"""
import argparse
import base64
import os
import pickle
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from dotenv import dotenv_values, set_key

from config import (
    APP_DIR,
    PRIVATE_KEY_ENV_FILE,
    PRIVATE_KEY_ENV_VAR,
    PUBLIC_KEY_PATH,
    RSA_KEY_SIZE,
)
from crypto_utils import count_plaintext_secrets


def _pickle_has_encrypted_data() -> bool:
    pkl = APP_DIR / "Saved.pkl"
    if not pkl.exists() or pkl.stat().st_size == 0:
        return False
    with open(pkl, "rb") as f:
        records = pickle.load(f)
    # Any secret that is not plaintext is encrypted.
    total = sum(
        (1 if isinstance(r.get("password"), str) else 0) + len(r.get("password_history") or [])
        for r in records.values() if isinstance(r, dict)
    )
    return count_plaintext_secrets(records) < total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="Overwrite existing keys.")
    args = parser.parse_args()

    existing_private = PRIVATE_KEY_ENV_FILE.exists() and dotenv_values(PRIVATE_KEY_ENV_FILE).get(PRIVATE_KEY_ENV_VAR)
    if (PUBLIC_KEY_PATH.exists() or existing_private) and not args.force:
        print(f"Keys already exist ({PUBLIC_KEY_PATH} and/or {PRIVATE_KEY_ENV_VAR} in {PRIVATE_KEY_ENV_FILE}).")
        print("Refusing to overwrite. Use --force if you really want new keys.")
        return 1

    if args.force and _pickle_has_encrypted_data():
        print("Saved.pkl already contains encrypted data. Replacing the keys would make it "
              "PERMANENTLY unreadable. Aborting.")
        return 1

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=RSA_KEY_SIZE)

    # Public key -> app config
    PUBLIC_KEY_PATH.write_bytes(
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )

    # Private key -> ~/.env (single-line base64 DER so it is .env friendly)
    private_b64 = base64.b64encode(
        private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    ).decode("ascii")

    PRIVATE_KEY_ENV_FILE.touch(mode=0o600, exist_ok=True)
    set_key(str(PRIVATE_KEY_ENV_FILE), PRIVATE_KEY_ENV_VAR, private_b64)
    os.chmod(PRIVATE_KEY_ENV_FILE, 0o600)

    print(f"Public key written to : {PUBLIC_KEY_PATH}")
    print(f"Private key written to: {PRIVATE_KEY_ENV_FILE} ({PRIVATE_KEY_ENV_VAR}, chmod 600)")
    print("\nIMPORTANT: back up the private key somewhere safe and offline. "
          "If it is lost, your saved passwords cannot be recovered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
