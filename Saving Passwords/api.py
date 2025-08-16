from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from StorePasswords import (
    SavedPasswords,
    dictPickleFile,
    generate_password,
    MIN_PASSWORD_LENGTH,
)

# Load persisted data on startup if present
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        pkl_path = Path(dictPickleFile)
        if pkl_path.exists():
            SavedPasswords.readFromPickle(str(pkl_path))
    except Exception:
        # If reading fails, continue with in-memory defaults
        pass
    yield
    SavedPasswords.dumpToPickle(dictPickleFile)

app = FastAPI(title="Password Manager API", version="1.0.0", lifespan=lifespan)

# Allow same-origin and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)    


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


@app.get("/api/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


class SaveRequest(BaseModel):
    title: str
    password: str
    email: Optional[str] = None


class RenameRequest(BaseModel):
    currentTitle: str
    newTitle: str


class GenerateRequest(BaseModel):
    length: int = Field(..., ge=MIN_PASSWORD_LENGTH)


@app.get("/api/titles", response_model=List[str])
async def list_titles() -> List[str]:
    return SavedPasswords.getPasswordTitles()


@app.get("/api/password/{title}")
async def get_password(title: str):
    if not SavedPasswords.checkIfTitleExists(title):
        raise HTTPException(status_code=404, detail="Title not found")
    return SavedPasswords.getPassword(title)


@app.get("/api/passwords")
async def get_all_passwords():
    # Expose all stored records
    return SavedPasswords.passwords


@app.post("/api/password")
async def save_password(req: SaveRequest):
    SavedPasswords.savePassword(req.title, req.password, email=req.email)
    try:
        SavedPasswords.dumpToPickle(dictPickleFile)
    except Exception:
        pass
    return {"status": "ok", "title": req.title}


@app.delete("/api/password/{title}")
async def delete_password(title: str):
    if not SavedPasswords.checkIfTitleExists(title):
        raise HTTPException(status_code=404, detail="Title not found")
    SavedPasswords.delPassword(title)
    SavedPasswords.dumpToPickle(dictPickleFile)
    return {"status": "ok"}


@app.patch("/api/title")
async def rename_title(req: RenameRequest):
    if not SavedPasswords.checkIfTitleExists(req.currentTitle):
        raise HTTPException(status_code=404, detail="Title not found")
    SavedPasswords.updatePasswordTitle(req.currentTitle, req.newTitle)
    SavedPasswords.dumpToPickle(dictPickleFile)
    return {"status": "ok", "newTitle": req.newTitle}


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    try:
        pwd = generate_password(req.length)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"password": pwd}
