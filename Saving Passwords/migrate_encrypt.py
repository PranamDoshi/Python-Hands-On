"""One-time migration: encrypt every existing `password` and `password_history` entry in Saved.pkl.

Steps:
  1. Copies Saved.pkl to a timestamped plaintext backup (chmod 600).
  2. Loads the file (plaintext values pass through), re-saves it encrypted.
  3. Verifies no plaintext secrets remain AND that decrypting gives back the original data.
     If verification fails, the original file is restored from the backup.

Safe to re-run: already-encrypted values are left untouched.

Usage:
    python migrate_encrypt.py
"""
import os
import pickle
import shutil
import sys
from datetime import datetime

from crypto_utils import count_plaintext_secrets, load_private_key, load_public_key
from StorePasswords import SavedPasswords, dictPickleFile


def main() -> int:
    if not os.path.exists(dictPickleFile) or os.path.getsize(dictPickleFile) == 0:
        print(f"Nothing to migrate: {dictPickleFile} is missing or empty.")
        return 0

    # Fail early (before touching anything) if either key is missing or they don't match.
    load_public_key()
    load_private_key()

    with open(dictPickleFile, "rb") as f:
        plaintext_count = count_plaintext_secrets(pickle.load(f))
    if plaintext_count == 0:
        print("All secrets are already encrypted. Nothing to do.")
        return 0

    backup = f"{dictPickleFile}.plaintext-backup-{datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(dictPickleFile, backup)
    os.chmod(backup, 0o600)

    try:
        SavedPasswords.readFromPickle(dictPickleFile)
        original = SavedPasswords.passwords
        SavedPasswords.dumpToPickle(dictPickleFile)

        with open(dictPickleFile, "rb") as f:
            remaining = count_plaintext_secrets(pickle.load(f))
        if remaining:
            raise RuntimeError(f"{remaining} secret(s) still in plaintext after migration")

        SavedPasswords.readFromPickle(dictPickleFile)
        if SavedPasswords.passwords != original:
            raise RuntimeError("Decrypted data does not match the original data")
    except Exception as exc:
        shutil.copy2(backup, dictPickleFile)
        print(f"Migration FAILED ({exc}). Original file restored from {backup}.")
        return 1

    print(f"Encrypted {plaintext_count} secret value(s) across {len(original)} record(s).")
    print(f"Verified round-trip decryption.")
    print(f"\nA PLAINTEXT backup was written to:\n  {backup}\n"
          "Delete it once you've confirmed the app works:  rm -P '" + backup + "'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
