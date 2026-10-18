# Render.com Deployment & Google Drive Storage Plan

This document details the architecture and click-by-click setup to:
1. **Snapshot the local version** via Git tag `v1.0-local` on `main` (so you can check out `git checkout v1.0-local` anytime you want the legacy local-file version).
2. **Migrate persistence exclusively to Google Drive** (`Saved.pkl` read and written directly in memory via Google Drive v3 API using a Google Cloud Service Account, with no dependency on a local `Saved.pkl` file).
3. **Deploy to Render.com (Free Tier)** at `https://<your-service>.onrender.com` (zero credit card required).
4. **Enforce Application Master Password Authentication**:
   - Mandatory environment-configured master password (`SAVING_PASSWORDS_AUTH_PASSWORD`).
   - Stateless `PBKDF2-HMAC-SHA256` + `HMAC-SHA256` signed `HttpOnly` session cookies (`vault_session`) that survive Render container restarts.
   - Sliding-window brute-force rate limiting per IP (`429 Too Many Requests` after 5 failed attempts in 5 minutes).
   - Full-screen **Unlock Vault** login UI and protected `/api/*` + `/docs` routes.

---

## Architecture Overview

```mermaid
flowchart LR
    User["User Browser\n(https://<service>.onrender.com)"] --> FastAPI["FastAPI Container\n(Render.com Free Tier)"]
    FastAPI -->|Verifies Master Password Session\nPBKDF2 + HMAC-SHA256 Cookie| AuthLayer["auth.py\n(SAVING_PASSWORDS_AUTH_PASSWORD)"]
    AuthLayer -->|RSA-3072 + AES-GCM\n(SAVING_PASSWORDS_PRIVATE_KEY)| Crypto["crypto_utils.py"]
    Crypto -->|Read in-memory on startup & refresh\nUpload in-memory on every mutation| GDrive["Google Drive v3 API\n(Saved.pkl: 1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A)"]
```

---

## Phase 0: Git Tag for Legacy Local Version (Done ✅)

Before modifying any code on `main`, we tagged the local-only commit (`f791730`) as **`v1.0-local`**:
- **How to run the local version anytime in the future:**
  ```bash
  git checkout v1.0-local
  uv run uvicorn api:app --reload
  ```

---

## Phase 1: Google Drive Service Account & Credential Configuration (Done ✅)

[`Saved.pkl`](file:///Users/pranamdoshi/git/Python-Hands-On/Saving%20Passwords/Saved.pkl) is stored exclusively in your Google Drive (`1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A`) and read/written in memory (`pickle.loads` / `pickle.dumps`) via the Google Drive v3 API—no local `.pkl` file is read or written by the application.

### Environment & Secret Configuration Matrix

| Variable | Required? | Purpose | Render.com Configuration |
| :--- | :---: | :--- | :--- |
| `SAVING_PASSWORDS_PRIVATE_KEY` | **Yes** | RSA-3072 Private Key (single-line base64 DER) | Environment Variable |
| `SAVING_PASSWORDS_AUTH_PASSWORD` | **Yes** | Master password required to unlock the web UI & API | Environment Variable |
| `GDRIVE_FILE_ID` | **Yes** | The Google Drive File ID of `Saved.pkl` | `1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A` |
| `GDRIVE_SERVICE_ACCOUNT_FILE` | **Yes** | Path to Service Account `.json` file | `/etc/secrets/gdrive-service-account.json` (via Render **Secret Files**) |
| `PORT` | **Yes** | Container port for Uvicorn | `8000` |

---

## Phase 2: Step-by-Step Guide to Set Up Render.com (Free Tier — No Credit Card Required)

### 2.1 Step 1: Create the Render Web Service & Connect GitHub
1. Go to [https://dashboard.render.com/](https://dashboard.render.com/) and sign in with **GitHub** (no credit card is required for Free Web Services).
2. In the top-right corner, click **New +** → select **Web Service**.
3. Select **Build and deploy from a Git repository** and click **Next**.
4. Find your **`Python-Hands-On`** repository and click **Connect**.

### 2.2 Step 2: Configure Monorepo Subdirectory & Docker Runtime
Because your project is inside the `Saving Passwords` subfolder of `Python-Hands-On`, configure these exact settings on the creation page:
1. **Name:** `saving-passwords-vault` (this gives you `https://saving-passwords-vault.onrender.com`).
2. **Region:** Choose the region closest to you (`Singapore (Southeast Asia)`, `Frankfurt (EU Central)`, `Ohio (US East)`, or `Oregon (US West)`).
3. **Branch:** `main`
4. **Root Directory:** Type `Saving Passwords` *(important: do **not** put quotes around it; Render scopes the Docker build context and auto-deploy triggers to `Saving Passwords/` so `COPY pyproject.toml uv.lock ./` resolves properly)*.
5. **Runtime:** Select **`Docker`**.
6. **Dockerfile Path:** Leave as `Dockerfile` (resolved relative to `Saving Passwords/`).
7. **Instance Type:** Select **Free** (`$0 / month`, `512 MB RAM`, `0.1 CPU`).

### 2.3 Step 3: Configure Environment Variables on Render
Scroll down to the **Environment Variables** section and click **Add Environment Variable** for each of the following:

| Key | Value to Paste |
| :--- | :--- |
| `SAVING_PASSWORDS_PRIVATE_KEY` | Run on Mac: `grep "^SAVING_PASSWORDS_PRIVATE_KEY=" ~/.env \| cut -d= -f2- \| pbcopy` and paste |
| `SAVING_PASSWORDS_AUTH_PASSWORD` | Choose a strong Master Password that you will type into the "Unlock Vault" login screen |
| `GDRIVE_FILE_ID` | `1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A` |
| `GDRIVE_SERVICE_ACCOUNT_FILE` | `/etc/secrets/gdrive-service-account.json` |
| `PORT` | `8000` |

### 2.4 Step 4: Upload the Google Service Account JSON as a Render "Secret File"
Still on the Render creation page, right below Environment Variables, find the **Secret Files** section:
1. Click **Add Secret File**.
2. **Filename:** `gdrive-service-account.json` *(Render mounts Secret Files inside Docker containers at `/etc/secrets/<Filename>`, matching `/etc/secrets/gdrive-service-account.json`)*.
3. **Contents:** Run this command on your Mac terminal to copy the JSON contents to your clipboard:
   ```bash
   pbcopy < ~/.config/saving-passwords/gdrive-service-account.json
   ```
   Then paste (`Cmd + V`) the multi-line JSON directly into the **Contents** box on Render.

### 2.5 Step 5: Configure Health Check & Deploy
1. Scroll down and click **Advanced** to expand advanced settings.
2. **Health Check Path:** Enter `/api/health`.
3. **Auto-Deploy:** Keep set to `Yes`.
4. Click **Create Web Service** at the bottom.
5. Wait ~2 minutes for the Docker build to finish until Render shows `Your service is live 🎉` at your `https://<your-service>.onrender.com` URL.

---

## Phase 3: Application Authentication & Security Specification (`auth.py` + `api.py` + `web/`)

Because Render Free Tier does not provide built-in basic auth at the platform level (that is a paid Render feature), authentication is built directly into your FastAPI backend and Web UI:

1. **Constant-Time Password Verification & Brute-Force Protection ([`auth.py`](file:///Users/pranamdoshi/git/Python-Hands-On/Saving%20Passwords/auth.py)):**
   - Hashes candidate passwords with `200,000` rounds of `PBKDF2-HMAC-SHA256` and compares using `secrets.compare_digest()`.
   - Blocks any IP after **5 failed login attempts within 5 minutes** (`HTTP 429 Too Many Requests` with `Retry-After` header).
2. **Stateless Signed Session Cookies (Survives Render Container Sleep/Wake):**
   - Signs session tokens (`v1.<exp>.<nonce>.<hmac_sha256>`) using a key derived from `SAVING_PASSWORDS_AUTH_PASSWORD` + `SAVING_PASSWORDS_PRIVATE_KEY`.
   - Stored in an `HttpOnly`, `SameSite=Lax`, `Secure` cookie (`vault_session`, default TTL 24 hours).
   - Because the signature is deterministic, your browser remains logged in even when the Render container spins down after 15 minutes of inactivity and wakes back up.
3. **Route Protection Matrix ([`api.py`](file:///Users/pranamdoshi/git/Python-Hands-On/Saving%20Passwords/api.py)):**

| Endpoint | Authentication Required? | Purpose |
| :--- | :---: | :--- |
| `GET /api/health` | **Public** | Render internal health probes |
| `GET /`, `GET /favicon.ico`, `GET /static/*` | **Public** | Serves UI shell so Unlock Vault modal can render |
| `GET /api/auth/status` | **Public** | Returns `{"authenticated": bool, "auth_required": true}` |
| `POST /api/auth/login` | **Public (Rate-Limited)** | Verifies master password & sets `vault_session` cookie |
| `POST /api/auth/logout` | **Public** | Clears `vault_session` cookie |
| `GET /api/titles`, `/api/passwords`, `/api/password/{title}` | **Required (`401`)** | Read decrypted vault data |
| `POST /api/password`, `DELETE /api/password/{title}`, `PATCH /api/title` | **Required (`401`)** | Mutate vault & upload to Google Drive |
| `POST /api/generate` | **Required (`401`)** | Password generator |
| `GET /docs`, `GET /openapi.json` | **Required (`401`)** | Swagger API documentation protected behind login |

---

## Phase 4: Implementation Checklist

- [x] **Step 0:** Create Git tag `v1.0-local` on `main` before cloud changes so the local-file version is preserved.
- [x] **Step 1 (`gdrive_storage.py` & `pyproject.toml`):** Add Google Drive API support (`google-auth` + `requests`) to download and upload `Saved.pkl` bytes in-memory by `GDRIVE_FILE_ID`.
- [x] **Step 2 (`config.py`, `StorePasswords.py`, `api.py`):** Update `readFromPickle()` and `dumpToPickle()` to read/write exclusively from Google Drive (`1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A`), and wire `GET /api/passwords?refresh=true` to re-sync from Google Drive.
- [x] **Step 3 (`auth.py` & `api.py`):** Implement mandatory `SAVING_PASSWORDS_AUTH_PASSWORD` verification, stateless HMAC session cookies, brute-force rate limiting, `/api/auth/{status,login,logout}`, and route protection across `/api/*` and `/docs`.
- [x] **Step 4 (`web/index.html`, `web/app.js`, `web/styles.css`):** Add the Unlock Vault login dialog, `401` interceptor, and sidebar Lock button.
- [x] **Step 5 (`Dockerfile` & `.gitignore`):** Update `Dockerfile` `CMD` to bind `${PORT:-8000}` with `--proxy-headers --forwarded-allow-ips='*'`, remove local `Saved.pkl` volume mounts/references, and verify Google Drive read/write with `GDRIVE_FILE_ID`.
