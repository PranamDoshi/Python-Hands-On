from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from auth import (
    check_rate_limit,
    clear_failed_attempts,
    clear_session_cookie,
    create_session_token,
    get_cf_access_config,
    get_client_ip,
    is_auth_configured,
    is_request_authenticated,
    record_failed_attempt,
    require_auth,
    set_session_cookie,
    verify_cf_access_jwt,
    verify_master_password,
)
from StorePasswords import (
    MIN_PASSWORD_LENGTH,
    SavedPasswords,
    generate_password,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load encrypted vault directly from Google Drive on startup.
    SavedPasswords.readFromPickle()
    yield


app = FastAPI(title="Password Manager API", version="1.0.0", lifespan=lifespan)


@app.middleware("http")
async def cloudflare_zero_trust_middleware(request: Request, call_next):
    # Always allow internal container health probes (/api/health)
    if request.url.path == "/api/health":
        return await call_next(request)

    issuer, expected_aud = get_cf_access_config()
    if issuer and expected_aud:
        cf_token = (
            request.headers.get("cf-access-jwt-assertion")
            or request.cookies.get("CF_Authorization")
        )
        if not cf_token:
            return JSONResponse(
                status_code=403,
                content={"detail": "Cloudflare Zero Trust Access authentication required."},
            )
        try:
            verify_cf_access_jwt(cf_token, issuer, expected_aud)
        except Exception as exc:
            return JSONResponse(
                status_code=403,
                content={"detail": f"Invalid Cloudflare Access token: {exc}"},
            )

    return await call_next(request)


# Serve static UI from ./web
static_dir = Path(__file__).parent / "web"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    index_html = static_dir / "index.html"
    if index_html.exists():
        return FileResponse(str(index_html))
    return HTMLResponse("<h1>Password Manager API</h1>")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    favicon_path = static_dir / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(str(favicon_path))
    raise HTTPException(status_code=404, detail="Favicon not found")


@app.get("/api/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


# ── Authentication Endpoints ────────────────────────────────────────────────
class LoginRequest(BaseModel):
    password: str


@app.get("/api/auth/status")
async def auth_status(request: Request):
    return {
        "authenticated": is_request_authenticated(request),
        "auth_required": True,
        "auth_configured": is_auth_configured(),
    }


@app.post("/api/auth/login")
async def login(req: LoginRequest, request: Request, response: Response):
    ip = get_client_ip(request)
    check_rate_limit(ip)
    if not verify_master_password(req.password):
        record_failed_attempt(ip)
        raise HTTPException(status_code=401, detail="Invalid master password")
    clear_failed_attempts(ip)
    token, exp = create_session_token()
    set_session_cookie(response, request, token)
    return {"status": "ok", "token": token, "expires_at": exp}


@app.post("/api/auth/logout")
async def logout(request: Request, response: Response):
    clear_session_cookie(response, request)
    return {"status": "ok"}


# ── Protected Vault Endpoints ───────────────────────────────────────────────
class SaveRequest(BaseModel):
    title: str
    password: str
    email: Optional[str] = None


class RenameRequest(BaseModel):
    currentTitle: str
    newTitle: str


class GenerateRequest(BaseModel):
    length: int = Field(..., ge=MIN_PASSWORD_LENGTH)


@app.get("/api/titles", response_model=List[str], dependencies=[Depends(require_auth)])
async def list_titles() -> List[str]:
    return SavedPasswords.getPasswordTitles()


@app.get("/api/password/{title}", dependencies=[Depends(require_auth)])
async def get_password(title: str):
    if not SavedPasswords.checkIfTitleExists(title):
        raise HTTPException(status_code=404, detail="Title not found")
    return SavedPasswords.getPassword(title)


@app.get("/api/passwords", dependencies=[Depends(require_auth)])
async def get_all_passwords(refresh: bool = Query(default=False)):
    if refresh:
        try:
            SavedPasswords.readFromPickle()
        except Exception as e:
            raise HTTPException(
                status_code=502, detail=f"Failed to sync from Google Drive: {e}"
            )
    return SavedPasswords.passwords


@app.post("/api/password", dependencies=[Depends(require_auth)])
async def save_password(req: SaveRequest):
    SavedPasswords.savePassword(req.title, req.password, email=req.email)
    try:
        SavedPasswords.dumpToPickle()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to persist password: {e}")
    return {"status": "ok", "title": req.title}


@app.delete("/api/password/{title}", dependencies=[Depends(require_auth)])
async def delete_password(title: str):
    if not SavedPasswords.checkIfTitleExists(title):
        raise HTTPException(status_code=404, detail="Title not found")
    SavedPasswords.delPassword(title)
    try:
        SavedPasswords.dumpToPickle()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to persist deletion: {e}")
    return {"status": "ok"}


@app.patch("/api/title", dependencies=[Depends(require_auth)])
async def rename_title(req: RenameRequest):
    if not SavedPasswords.checkIfTitleExists(req.currentTitle):
        raise HTTPException(status_code=404, detail="Title not found")
    SavedPasswords.updatePasswordTitle(req.currentTitle, req.newTitle)
    try:
        SavedPasswords.dumpToPickle()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to persist rename: {e}")
    return {"status": "ok", "newTitle": req.newTitle}


@app.post("/api/generate", dependencies=[Depends(require_auth)])
async def generate(req: GenerateRequest):
    try:
        pwd = generate_password(req.length)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"password": pwd}
