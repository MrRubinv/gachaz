import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from utils.gacha import perform_pulls


class PullRequest(BaseModel):
    count: int = Field(ge=1, le=10, description="ludka")
    banner: str = Field(default="standard", description="Banner name: vivian")


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


if __name__ == "__main__":
    # Local dev server: python main.py
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reload=True)


