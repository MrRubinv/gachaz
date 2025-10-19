import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv

from utils.gacha import perform_pulls


def _safe_load_dotenv() -> bool:
    try:
        path = find_dotenv(usecwd=True)
        if not path:
            return False
        # Detect UTF-16/UTF-32 BOM and skip if present
        with open(path, "rb") as fh:
            head = fh.read(4)
        if head.startswith(b"\xff\xfe") or head.startswith(b"\xfe\xff") or head.startswith(b"\x00\x00\xfe\xff") or head.startswith(b"\xff\xfe\x00\x00"):
            print("[warn] .env appears to have a BOM or non-UTF8 encoding; skipping load.")
            return False
        return load_dotenv(dotenv_path=path)
    except Exception as e:
        print(f"[warn] Failed to load .env: {e}")
        return False


_safe_load_dotenv()


class PullRequest(BaseModel):
    count: int = Field(ge=1, le=10, description="Number of pulls to perform (1-10)")
    banner: str = Field(default="standard", description="Banner name, e.g., 'standard'")


class PullResult(BaseModel):
    rarity: int
    name: str
    pity4At: int
    pity5At: int


class PullsResponse(BaseModel):
    results: List[PullResult]
    summary: dict


app = FastAPI(title="ZZZ-like Gacha API", version="0.1.0")

# Allow embedding in Telegram WebView; CORS not strictly needed for same-origin, but safe for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    commit = os.environ.get("RENDER_GIT_COMMIT") or os.environ.get("GIT_SHA") or "unknown"
    ts = datetime.now(timezone.utc).isoformat()
    return {"status": "ok", "message": "API is working", "commit": commit, "timestamp": ts}

@app.post("/api/pull", response_model=PullsResponse)
def pull_api(payload: PullRequest) -> PullsResponse:
    pulls = perform_pulls(count=payload.count, banner=payload.banner)
    results = [
        PullResult(rarity=p["rarity"], name=p["name"], pity4At=p["pity4At"], pity5At=p["pity5At"]) for p in pulls["results"]
    ]
    return PullsResponse(results=results, summary=pulls["summary"])


# Serve the Telegram WebApp frontend from / (root)
webapp_dir = os.path.join(os.path.dirname(__file__), "webapp")
if os.path.isdir(webapp_dir):
    app.mount("/", StaticFiles(directory=webapp_dir, html=True), name="webapp")
else:
    # Fallback route for root
    @app.get("/")
    def read_root():
        return {"message": "WebApp not found. Check webapp directory."}

# Also add a direct route for index.html
@app.get("/index.html")
def serve_index():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(webapp_dir, "index.html"))


if __name__ == "__main__":
    # Local dev server: python main.py
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


