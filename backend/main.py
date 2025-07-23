from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List

from schemas import RequestOut, RequestCreate
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
def get_all_requests():
    return db.get_all_requests()


@app.get("/requests/user/{user_id}", response_model=List[RequestOut])
def get_requests_by_user(user_id: int):
    requests = db.get_request(user_id)
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found for this user")
    return requests


@app.post("/requests", response_model=RequestOut)
def create_request(data: RequestCreate):
    return db.create_request(data)


@app.put("/requests/{request_id}", response_model=RequestOut)
def update_request(request_id: int, data: RequestCreate):
    try:
        return db.update_request(request_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/requests/{request_id}", response_model=bool)
def delete_request(request_id: int):
    success = db.delete_request(request_id)
    if not success:
        raise HTTPException(status_code=404, detail="Request not found")
    return success


@app.get("/{file_path:path}", response_class=FileResponse)
def get_file(file_path: str):
    full_path = Path("frontend") / file_path
    if full_path.is_file():
        return FileResponse(path=full_path)
    raise HTTPException(status_code=404, detail="File Not Found")
