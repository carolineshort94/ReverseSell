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


@app.post("/api/update_request", response_model=RequestUpdate | None)
async def update_request(
    request_id: int,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    quantity: int | None = None,
    price_range: int | None = None,
    location: str | None = None,
    location_range: str | None = None,
    expiry_date: datetime | None = None,
):
    return db.update_request(
        request_id,
        title,
        description,
        status,
        quantity,
        price_range,
        location,
        location_range,
        expiry_date,
    )


@app.get("/{file_path}", response_class=FileResponse)
def get_file(file_path: str):
    if Path("frontend/" + file_path).is_file():
        return "frontend/" + file_path
    raise HTTPException(status_code=404, detail="File Not Found")
