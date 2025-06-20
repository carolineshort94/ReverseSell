from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    status,
    Request,
    UploadFile,
    File,
    Form,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from pathlib import Path
import os
import json
from starlette.responses import JSONResponse
from schemas import (
    RequestCreate,
    RequestUpdate,
    ResquestOut,
    OfferCreate,
    OfferUpdate,
    OfferOut,
    ProductImageCreate,
    MessageCreate,
)
from models import (
    DBRequest,
    DBCategory,
    DBOffer,
    DBProduct_image,
    DBMessage,
)
from sqlalchemy.orm import Session
from rich import print  # For rich console output
import db

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/requests", response_model=list[ResquestOut])
async def get_request(user_id: int):

    return db.get_request(user_id)


@app.post("/api/update_request", response_model=ResquestOut)
async def update_request(request_id: int, description: str, status: str, ):
    return db.update_request(request_id, description, status,


@app.get("/{file_path}", response_class=FileResponse)
def get_file(file_path: str):
    if Path("frontend/" + file_path).is_file():
        return "frontend/" + file_path
    raise HTTPException(status_code=404, detail="File Not Found")
