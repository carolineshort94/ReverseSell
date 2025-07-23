from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
from pathlib import Path
from typing import Optional

from schemas import RequestOut
from auth import auth_router
import db

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth route
app.include_router(auth_router, prefix="/api")


@app.get("/requests", response_model=List[RequestOut])
def get_requests(user_id: int = Query(...)):
    return db.get_request(user_id)


@app.get("/{file_path:path}", response_class=FileResponse)
def get_file(file_path: str):
    full_path = Path("frontend") / file_path
    if full_path.is_file():
        return FileResponse(path=full_path)
    raise HTTPException(status_code=404, detail="File Not Found")
