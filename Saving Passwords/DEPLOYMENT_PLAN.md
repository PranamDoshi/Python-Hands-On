# Cloud Deployment, Zero Trust & Google Drive Storage Plan

This document details the complete architecture and click-by-click setup to:
1. **Snapshot the local version** via Git tag `v1.0-local` on `main` (so you can check out `git checkout v1.0-local` anytime you want the legacy local-file version).
2. **Migrate persistence exclusively to Google Drive** (`Saved.pkl` read and written directly via Google Drive v3 API using a Google Cloud Service Account, with no dependency on a local `Saved.pkl` file).
3. **Deploy to Render.com (Free Tier)** from the `Saving Passwords` subfolder of the `Python-Hands-On` repository.
4. **Enforce Two-Layer Authentication**:
   - **Layer 1 (Edge):** **Cloudflare Zero Trust (Cloudflare Access)** via Custom Domain CNAME + Origin JWT verification (`Cf-Access-Jwt-Assertion`) so no one can bypass Cloudflare by visiting the raw `*.onrender.com` URL.
   - **Layer 2 (Application):** Mandatory environment-configured master password (`SAVING_PASSWORDS_AUTH_PASSWORD`), stateless HMAC-signed `HttpOnly` session cookies that survive container scale-to-zero restarts, brute-force rate limiting, and an **Unlock Vault** login UI.

---

## Architecture Overview

```mermaid
flowchart LR
    User["User Browser\n(vault.yourdomain.com)"] --> CFAccess["Layer 1: Cloudflare Zero Trust\n(Edge OTP / Google OAuth)"]
    CFAccess -->|CNAME + Cf-Access-Jwt-Assertion| FastAPI["FastAPI Container\n(Render.com Free Tier)"]
    FastAPI -->|1. Verifies CF JWT (RS256)\n2. Verifies Master Password Session| AuthLayer["Layer 2: auth.py\n(SAVING_PASSWORDS_AUTH_PASSWORD)"]
    AuthLayer -->|RSA-3072 + AES-GCM\n(SAVING_PASSWORDS_PRIVATE_KEY)| Crypto["crypto_utils.py"]
    Crypto -->|Read in-memory on startup & refresh\nUpload in-memory on every mutation| GDrive["Google Drive v3 API\n(Saved.pkl by GDRIVE_FILE_ID)"]
```

---

## Phase 0: Git Tag for Legacy Local Version (Done ✅)

Before modifying any code on `main`, we tagged the current commit (`f791730`) as **`v1.0-local`**:
- **Push the tag to GitHub:** `git push origin v1.0-local`
- **How to run the local version anytime in the future:**
  ```bash
  git checkout v1.0-local
  uv run uvicorn api:app --reload
  ```

---

## Phase 1: Google Drive Service Account & Credential Configuration (Done ✅)

[`Saved.pkl`](file:///Users/pranamdoshi/git/Python-Hands-On/Saving%20Passwords/Saved.pkl) is stored exclusively in your Google Drive and read/written in memory (`io.BytesIO` + `pickle`) via the Google Drive v3 API—no local `.pkl` file is read or written by the application.

### 1.1 Service Account & Google Drive Setup Summary
1. **Google Cloud Project:** Created with **Google Drive API** enabled.
2. **Service Account JSON Key:** Saved locally outside the repo at `~/.config/saving-passwords/gdrive-service-account.json` (`chmod 600`).
3. **Google Drive File:** `Saved.pkl` uploaded to Google Drive and shared with the Service Account email with **Editor** permission.

### 1.2 Environment & Secret Configuration Matrix

| Variable | Required? | Purpose | Render.com Configuration | Local Verification (`~/.env`) |
| :--- | :---: | :--- | :--- | :--- |
| `SAVING_PASSWORDS_PRIVATE_KEY` | **Yes** | RSA-3072 Private Key (single-line base64 DER) | Environment Variable | Already in `~/.env` |
| `SAVING_PASSWORDS_AUTH_PASSWORD` | **Yes** | Master password required to unlock the web UI & API | Environment Variable | Set in `~/.env` |
| `GDRIVE_FILE_ID` | **Yes** | The Google Drive File ID of `Saved.pkl` | Environment Variable | Set in `~/.env` |
| `GDRIVE_SERVICE_ACCOUNT_FILE` | **Yes** | Path to Service Account `.json` file | `/etc/secrets/gdrive-service-account.json` (via Render **Secret Files**) | `/Users/pranamdoshi/.config/saving-passwords/gdrive-service-account.json` |
| `CF_ACCESS_TEAM_DOMAIN` | **Yes** (Cloud) | Your Cloudflare Zero Trust team domain (e.g. `myteam`) | Environment Variable | Optional for local test |
| `CF_ACCESS_AUD` | **Yes** (Cloud) | 64-char Application Audience (`AUD`) tag from Cloudflare Access | Environment Variable | Optional for local test |

---

## Phase 2: Step-by-Step Guide to Set Up Render.com (Free Tier)

Follow these exact steps once we push the updated code to your GitHub repository:

### 2.1 Step 1: Create the Render Web Service & Connect GitHub
1. Go to [https://dashboard.render.com/](https://dashboard.render.com/) and sign in with **GitHub** (no credit card is required).
2. In the top-right corner, click **New +** → select **Web Service**.
3. Select **Build and deploy from a Git repository** and click **Next**.
4. Find your **`Python-Hands-On`** repository and click **Connect**.

### 2.2 Step 2: Configure Monorepo Subdirectory & Docker Runtime
Because your project is inside the `Saving Passwords` subfolder of `Python-Hands-On`, configure these exact settings on the creation page:
1. **Name:** `saving-passwords-vault` (this creates `https://saving-passwords-vault.onrender.com`).
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
| `SAVING_PASSWORDS_PRIVATE_KEY` | Output of: `grep SAVING_PASSWORDS_PRIVATE_KEY ~/.env \| cut -d= -f2-` |
| `SAVING_PASSWORDS_AUTH_PASSWORD` | Your chosen Master Password for the "Unlock Vault" login screen |
| `GDRIVE_FILE_ID` | `1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A` |
| `GDRIVE_SERVICE_ACCOUNT_FILE` | `/etc/secrets/gdrive-service-account.json` |
| `PORT` | `8000` |

*(You will also add `CF_ACCESS_TEAM_DOMAIN` and `CF_ACCESS_AUD` here in Phase 3 Step 4 below).*

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
5. Wait ~2 minutes for the Docker build to finish until Render shows `Your service is live 🎉`.

---

## Phase 3: Step-by-Step Guide to Set Up Cloudflare Custom Domain & Zero Trust Access

Using **Custom Domain CNAME + Cloudflare Zero Trust Access** ensures that whenever you visit `https://vault.yourdomain.com`, Cloudflare first authenticates your identity at the edge, and then forwards the request to Render—automatically waking up the sleeping Render container when needed.

### 3.1 Step 1: Initialize Cloudflare Zero Trust (Free Plan)
1. Log into the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. In the left sidebar, click **Zero Trust** (opens [https://one.dash.cloudflare.com/](https://one.dash.cloudflare.com/)).
3. If opening Zero Trust for the first time:
   - Choose a **Team name** (e.g., `pranam-vault` → your team domain is `pranam-vault.cloudflareaccess.com`). **Save this team name** as your `CF_ACCESS_TEAM_DOMAIN`.
   - Select the **Zero Trust Free Plan** (`$0/month` for up to 50 users).
4. Under **Settings → Authentication → Login methods**, confirm **One-time PIN (OTP)** is enabled (Cloudflare will email a 6-digit login code to your allowed email address; you can also optionally add **Google** OAuth here).

### 3.2 Step 2: Connect Your Subdomain (`vault.yourdomain.com`) to Render
> [!IMPORTANT]
> **Follow this exact order** (starting with Grey Cloud, verifying the cert on Render, setting SSL to `Full (Strict)`, and then turning on Orange Cloud) so Render's Let's Encrypt certificate issues cleanly without redirect loops.

1. In your **Render Dashboard** → click your `saving-passwords-vault` service → go to **Settings** → scroll down to **Custom Domains**.
2. Click **+ Add Custom Domain**, enter your chosen subdomain (e.g., `vault.yourdomain.com`), and click **Save**.
3. Render will display the CNAME target: `<your-service>.onrender.com`.
4. Open [Cloudflare Dashboard](https://dash.cloudflare.com/) → click your domain (`yourdomain.com`) → go to **DNS → Records**.
5. Click **+ Add record**:
   - **Type:** `CNAME`
   - **Name:** `vault` (or whatever subdomain prefix you chose)
   - **Target:** `<your-service>.onrender.com`
   - **Proxy status:** Toggle **OFF** so it says **DNS only (Grey Cloud ☁️)** initially.
   - Click **Save**.
6. Return to **Render → Settings → Custom Domains**, click **Verify** next to `vault.yourdomain.com`, and wait ~1–2 minutes until Render shows **Certificate Issued**.
7. Back in **Cloudflare Dashboard** for `yourdomain.com`:
   - Go to **SSL/TLS → Overview** and set encryption mode to **Full (Strict)** *(prevents `ERR_TOO_MANY_REDIRECTS`)*.
   - Go back to **DNS → Records**, edit the `vault` `CNAME` record, toggle **Proxy status ON (Proxied / Orange Cloud 🍊)**, and click **Save**.

### 3.3 Step 3: Create the Self-Hosted Application in Cloudflare Zero Trust
1. In [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/), go to **Access → Applications**.
2. Click **Add an application** → select **Self-hosted**.
3. **Tab 1 — Application Configuration:**
   - **Application name:** `Password Vault`
   - **Session Duration:** `24 hours`
   - Under **Public hostname**, click **+ Add public hostname**:
     - **Subdomain:** `vault`
     - **Domain:** `yourdomain.com`
     - **Path:** *(leave empty so the entire domain is protected)*
   - Click **Next** at the bottom.
4. **Tab 2 — Access Policies:**
   - **Policy name:** `Allow Only Me`
   - **Action:** `Allow`
   - Under **Configure rules → Include**:
     - **Selector:** Select **`Emails`**
     - **Emails:** Enter your personal email address.
   - Click **Next** at the bottom.
5. **Tab 3 — Setup (Cookie Settings):**
   - **SameSite Attribute:** Select `Lax`
   - **HTTP Only:** Keep toggled **ON**
   - Click **Add application**.
6. **Keep Let's Encrypt 60-Day Auto-Renewal Working:**
   - Still in **Access → Applications**, click **Add an application → Self-hosted** once more to allow Let's Encrypt HTTP-01 renewal challenges:
     - **Application name:** `Password Vault ACME Renewal`
     - **Subdomain:** `vault`, **Domain:** `yourdomain.com`, **Path:** `.well-known/acme-challenge/*`
     - **Policy name:** `Bypass ACME`, **Action:** `Bypass`, **Include Selector:** `Everyone`.
     - Save. This ensures Render can renew your SSL cert automatically every 60 days without Cloudflare Access blocking the `.well-known/acme-challenge/` path.

### 3.4 Step 4: Enable Origin Bypass Protection on Render (`CF_ACCESS_AUD`)
Even with Cloudflare Access protecting `vault.yourdomain.com`, your raw `<your-service>.onrender.com` URL still exists on the internet. To block anyone who tries to visit `*.onrender.com` directly:
1. In **Zero Trust → Access → Applications**, click on your **`Password Vault`** application → **Overview**.
2. Copy the **Application Audience (AUD) Tag** (a 64-character hex string).
3. Go to **Render Dashboard → `saving-passwords-vault` → Environment** and add:
   - `CF_ACCESS_TEAM_DOMAIN` = `<your-team-name>` (e.g., `pranam-vault`)
   - `CF_ACCESS_AUD` = `<paste the 64-character AUD tag>`
4. Click **Save Changes**. FastAPI will now cryptographically verify Cloudflare's `Cf-Access-Jwt-Assertion` RS256 header on every request (except `/api/health` for Render's internal health checker) and return `403 Forbidden` to any direct `*.onrender.com` traffic.

---

## Phase 4: Two-Layer App Authentication & Storage Specification

### 4.1 Pure Google Drive Storage (`gdrive_storage.py` + `StorePasswords.py`)
- Removes all reliance on a local `Saved.pkl` file.
- `readFromPickle()` downloads the binary `.pkl` stream directly from Google Drive (`files().get_media(fileId=GDRIVE_FILE_ID)`), unpickles the encrypted dictionary in memory, and decrypts entries using `SAVING_PASSWORDS_PRIVATE_KEY`.
- `dumpToPickle()` encrypts all records with `public_key.pem`, serializes them to an in-memory `io.BytesIO` buffer via `pickle.dump`, and uploads directly to Google Drive (`files().update(fileId=GDRIVE_FILE_ID, media_body=...)`) on every mutation (`POST /api/password`, `DELETE /api/password/{title}`, `PATCH /api/title`).
- Clicking **Refresh** in the UI (`GET /api/passwords?refresh=true`) re-fetches the latest file from Google Drive into memory.

### 4.2 Two-Layer Security Matrix (`auth.py` + `api.py` + `web/`)

| Endpoint | Layer 1: Cloudflare Access JWT (`CF_ACCESS_AUD` set) | Layer 2: App Master Password (`SAVING_PASSWORDS_AUTH_PASSWORD`) | Purpose |
| :--- | :---: | :---: | :--- |
| `GET /api/health` | **Exempt (Public)** | **Exempt (Public)** | Render internal health probes |
| `GET /`, `GET /favicon.ico`, `GET /static/*` | **Required (`403`)** | **Public** | Serves UI shell so Unlock Vault modal can render |
| `GET /api/auth/status` | **Required (`403`)** | **Public** | Returns `{"authenticated": bool, "auth_required": true}` |
| `POST /api/auth/login` | **Required (`403`)** | **Public (Rate-Limited)** | Verifies master password & sets `vault_session` cookie |
| `POST /api/auth/logout` | **Required (`403`)** | **Public** | Clears `vault_session` cookie |
| `GET /api/titles`, `/api/passwords`, `/api/password/{title}` | **Required (`403`)** | **Required (`401`)** | Read decrypted vault data |
| `POST /api/password`, `DELETE /api/password/{title}`, `PATCH /api/title` | **Required (`403`)** | **Required (`401`)** | Mutate vault & upload to Google Drive |
| `POST /api/generate` | **Required (`403`)** | **Required (`401`)** | Password generator |

---

## Phase 5: Implementation Checklist

- [x] **Step 0:** Create Git tag `v1.0-local` on `main` before cloud changes so the local-file version is preserved.
- [x] **Step 1 (`gdrive_storage.py` & `pyproject.toml`):** Add Google Drive API support (`google-auth` + `requests`) to download and upload `Saved.pkl` bytes in-memory by `GDRIVE_FILE_ID`.
- [x] **Step 2 (`config.py`, `StorePasswords.py`, `api.py`):** Update `readFromPickle()` and `dumpToPickle()` to read/write exclusively from Google Drive (`1ogv-rvwzuX4VRxhW1bnp-cdItL2rDx0A`), and wire `GET /api/passwords?refresh=true` to re-sync from Google Drive.
- [x] **Step 3 (`auth.py` & `api.py`):** Implement mandatory `SAVING_PASSWORDS_AUTH_PASSWORD` verification, stateless HMAC session cookies, brute-force rate limiting, `/api/auth/{status,login,logout}`, route protection across `/api/*`, and `Cf-Access-Jwt-Assertion` verification.
- [x] **Step 4 (`web/index.html`, `web/app.js`, `web/styles.css`):** Add the Unlock Vault login dialog, `401` interceptor, and sidebar Lock button.
- [x] **Step 5 (`Dockerfile` & `.gitignore`):** Update `Dockerfile` `CMD` to bind `${PORT:-8000}` with `--proxy-headers --forwarded-allow-ips='*'`, remove local `Saved.pkl` volume mounts/references, and verify Google Drive read/write with `GDRIVE_FILE_ID`.
