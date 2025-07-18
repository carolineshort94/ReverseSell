from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
from pathlib import Path
from schemas import RequestUpdate
from auth import auth_router
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


# Auth route
app.include_router(auth_router, prefix="/api")


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
