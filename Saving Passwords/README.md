# Password Manager

A lightweight password manager with a FastAPI backend and a simple web UI. Data is persisted to a local pickle file (`Saved.pkl`). The original terminal-based workflow in `StorePasswords.py` remains intact.


## Project Structure

- `api.py`
  - FastAPI app serving REST endpoints and the static UI.
  - Loads `Saved.pkl` on startup (if present) and persists on shutdown.
- `StorePasswords.py`
  - Core password logic and data model.
  - Also provides an interactive CLI menu if run directly.
- `StorePasswords_python39.py`
  - Python 3.9 compatible variant of the core logic.
- `Saved.pkl`
  - On-disk persistence of the in-memory passwords dictionary.
- `web/`
  - `index.html` – single-page UI.
  - `app.js` – frontend interactions (CRUD + generator).
  - `styles.css` – styles for the UI.
- `Dockerfile`
  - Container definition (Python 3.11 slim) to run the API/UI.
- `docker-compose.yml`
  - Exposes port 8000 and bind-mounts `Saved.pkl` for persistence.
- `run-compose.sh`
  - Convenience script to start/stop the app with Docker Compose. Creates an empty `Saved.pkl` if not present.
- `requirements.txt`
  - Python dependencies.
- `TestingCodes/`
  - Misc. sample/testing scripts (not required for normal use).


## How to Run

### 1) Local (Python)
Prereqs: Python 3.11+ recommended (3.9+ supported); pip

```bash
# optional: create and activate a virtual env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Run the API with auto-reload for development
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Open the UI at: http://localhost:8000

API docs (Swagger): http://localhost:8000/docs

Note: If `Saved.pkl` does not exist, it will be created when the app saves for the first time.


### 2) Docker
Prereqs: Docker Desktop

```bash
# Build
docker build -t password-manager:latest .

# Run (bind-mount the data file for persistence)
docker run --rm \
  -p 8000:8000 \
  -v "$(pwd)/Saved.pkl:/app/Saved.pkl" \
  password-manager:latest
```

Open the UI at: http://localhost:8000


### 3) Docker Compose
```bash
# Using the helper script (auto-detects docker compose)
bash ./run-compose.sh --build   # add -d to run detached

# Or directly
docker compose up --build       # docker-compose up --build (legacy)

# Stop
bash ./run-compose.sh down
# or: docker compose down
```


### 4) Terminal (CLI) mode
The original interactive CLI is still available:

```bash
python StorePasswords.py
```

This uses the same `Saved.pkl` file for persistence.


## UI Usage
- Add/Update: Use the form under "Add / Update Password". Saving an existing title updates the password (and appends to password history).
- View: Click a title under "Saved Passwords" to open Details.
- Edit in Details: Change the password field and click "Update".
- Rename: Click "Rename" in the details header.
- Delete: Click "Delete" in the details header.
- Generate: Use the generator section or the quick Generate button in the form.


## API Reference (brief)
- `GET /` – Serves the web UI.
- `GET /api/health` – Health check.
- `GET /api/titles` – List all titles.
- `GET /api/password/{title}` – Get a single record by title.
- `GET /api/passwords` – Dump all stored records.
- `POST /api/password` – Create or update a record.
  - Body: `{ "title": str, "password": str, "email": Optional[str] }`
- `DELETE /api/password/{title}` – Delete a record.
- `PATCH /api/title` – Rename a title.
  - Body: `{ "currentTitle": str, "newTitle": str }`
- `POST /api/generate` – Generate a password.
  - Body: `{ "length": int }` (min length enforced)


## Data Model (per title)
A record is stored roughly as:

```json
{
  "password": "<current_password>",
  "password_history": ["yy-mm-dd_<password>", ...],
  "title_history": ["yy-mm-dd_<title>", ...],
  "email": "name@example.com"
}
```

Notes:
- Updating a password appends to `password_history`.
- Renaming a title appends to `title_history`.


## Security Notes
- Data is persisted to a local pickle file (`Saved.pkl`) and is not encrypted. Do not use this for sensitive production secrets.
- Intended for local/offline experimentation. If exposing the API, review and tighten CORS and implement encryption/secrets management.


## Troubleshooting
- Port already in use: Change `--port` in the uvicorn command or stop the conflicting service.
- Permission errors on `Saved.pkl`: Ensure the file is writable by the running user or update the bind mount/file permissions.
- UI not loading: Verify the server is running and reachable at http://localhost:8000.
