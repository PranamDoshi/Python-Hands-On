"""Google Drive v3 storage backend for Saving Passwords.

Reads and writes the encrypted ``Saved.pkl`` binary payload directly in memory
against Google Drive using a Google Cloud Service Account. No local ``.pkl``
file is read or written.
"""
import base64
import json
import os
from pathlib import Path
from typing import Optional

from dotenv import dotenv_values
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

from config import (
    DEFAULT_GDRIVE_FILE_ID,
    GDRIVE_FILE_ID_ENV_VAR,
    GDRIVE_SERVICE_ACCOUNT_B64_ENV_VAR,
    GDRIVE_SERVICE_ACCOUNT_FILE_ENV_VAR,
    LOCAL_SERVICE_ACCOUNT_PATH,
    PRIVATE_KEY_ENV_FILE,
    RENDER_SECRET_FILE_PATH,
)

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]
_DRIVE_FILES_API = "https://www.googleapis.com/drive/v3/files"
_DRIVE_UPLOAD_API = "https://www.googleapis.com/upload/drive/v3/files"

_authorized_session: Optional[AuthorizedSession] = None


def _read_setting(var_name: str) -> Optional[str]:
    """Read an environment variable or fallback to ~/.env if present."""
    val = os.environ.get(var_name)
    if not val and PRIVATE_KEY_ENV_FILE.exists():
        val = dotenv_values(PRIVATE_KEY_ENV_FILE).get(var_name)
    if val:
        val = val.strip()
    return val or None


def get_gdrive_file_id() -> str:
    """Return the configured Google Drive file ID for Saved.pkl."""
    file_id = _read_setting(GDRIVE_FILE_ID_ENV_VAR) or DEFAULT_GDRIVE_FILE_ID
    if not file_id:
        raise RuntimeError(
            f"Google Drive file ID is not configured. Set {GDRIVE_FILE_ID_ENV_VAR}."
        )
    return file_id


def _load_service_account_credentials() -> service_account.Credentials:
    """Load Service Account credentials from B64 env var or JSON file path."""
    b64_val = _read_setting(GDRIVE_SERVICE_ACCOUNT_B64_ENV_VAR)
    if b64_val:
        try:
            raw_json = base64.b64decode(b64_val).decode("utf-8")
            info = json.loads(raw_json)
            return service_account.Credentials.from_service_account_info(
                info, scopes=DRIVE_SCOPES
            )
        except Exception as exc:
            raise RuntimeError(
                f"Failed to parse {GDRIVE_SERVICE_ACCOUNT_B64_ENV_VAR}: {exc}"
            ) from exc

    configured_path = _read_setting(GDRIVE_SERVICE_ACCOUNT_FILE_ENV_VAR)
    candidates = []
    if configured_path:
        candidates.append(Path(configured_path).expanduser())
    candidates.append(RENDER_SECRET_FILE_PATH)
    candidates.append(LOCAL_SERVICE_ACCOUNT_PATH)

    for candidate in candidates:
        if candidate.is_file():
            return service_account.Credentials.from_service_account_file(
                str(candidate), scopes=DRIVE_SCOPES
            )

    checked = ", ".join(str(p) for p in candidates)
    raise RuntimeError(
        "Google Drive Service Account credentials not found. "
        f"Set {GDRIVE_SERVICE_ACCOUNT_FILE_ENV_VAR} or {GDRIVE_SERVICE_ACCOUNT_B64_ENV_VAR} "
        f"(checked paths: {checked})."
    )


def _get_session() -> AuthorizedSession:
    """Return a cached AuthorizedSession that auto-refreshes OAuth2 tokens."""
    global _authorized_session
    if _authorized_session is None:
        creds = _load_service_account_credentials()
        _authorized_session = AuthorizedSession(creds)
    return _authorized_session


def download_pickle_bytes(file_id: Optional[str] = None) -> bytes:
    """Download the raw encrypted Saved.pkl bytes from Google Drive."""
    target_id = file_id or get_gdrive_file_id()
    session = _get_session()
    url = f"{_DRIVE_FILES_API}/{target_id}"
    resp = session.get(
        url,
        params={"alt": "media", "supportsAllDrives": "true"},
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(
            f"Google Drive download failed (HTTP {resp.status_code}) for file {target_id}: "
            f"{resp.text[:300]}"
        )
    return resp.content


def upload_pickle_bytes(data: bytes, file_id: Optional[str] = None) -> None:
    """Upload the encrypted Saved.pkl bytes in-memory to Google Drive."""
    target_id = file_id or get_gdrive_file_id()
    session = _get_session()
    url = f"{_DRIVE_UPLOAD_API}/{target_id}"
    resp = session.patch(
        url,
        params={"uploadType": "media", "supportsAllDrives": "true"},
        headers={"Content-Type": "application/octet-stream"},
        data=data,
        timeout=30,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(
            f"Google Drive upload failed (HTTP {resp.status_code}) for file {target_id}: "
            f"{resp.text[:300]}"
        )
