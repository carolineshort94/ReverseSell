from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List

from schemas import (
    RequestOut,
    RequestCreate,
    RequestUpdate,
    OfferCreate,
    OfferOut,
    MessageCreate,
    MessageOut,
    AccountOut,
)
from auth import auth_router
import db

app = FastAPI()

origins = ["http://localhost:8000", "http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth route
app.include_router(auth_router, prefix="/api")


@app.get("/me", response_model=AccountOut)
def get_me(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = db.get_current_user(session_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session token")
    return user


@app.get("/requests", response_model=List[RequestOut])
def get_all_requests():
    return db.get_all_requests()


@app.get("/requests/user/{user_id}", response_model=List[RequestOut])
def get_requests_by_user(user_id: int):
    requests = db.get_requests_by_user(user_id)
    if not requests:
        raise HTTPException(status_code=200, detail="No requests found for this user")
    return requests


@app.post("/requests", response_model=RequestOut)
def create_request(data: RequestCreate):
    return db.create_request(data)


@app.put("/requests/{request_id}", response_model=RequestOut)
def update_request(request_id: int, data: RequestUpdate):
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


@app.post("/offers", response_model=OfferOut)
def create_offer(data: OfferCreate):
    return db.create_offer(data)


@app.get("/offers/request/{request_id}", response_model=List[OfferOut])
def get_offers_by_request(request_id: int):
    offers = db.get_offers_by_request(request_id)
    if not offers:
        raise HTTPException(status_code=404, detail="No offers found for this request")
    return offers


@app.get("/offers/user/{user_id}", response_model=List[OfferOut])
def get_offers_by_user(user_id: int):
    offers = db.get_offers_by_user(user_id)
    if not offers:
        raise HTTPException(status_code=404, detail="No offers found for this user")
    return offers


@app.put("/offers/{offer_id}", response_model=OfferOut)
def update_offer(offer_id: int, data: OfferCreate):
    try:
        return db.update_offer(offer_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/messages", response_model=MessageOut)
def create_message(data: MessageCreate):
    return db.send_message(data)


@app.get("/messages/offer/{offer_id}", response_model=List[MessageOut])
def get_messages_by_offer(offer_id: int):
    messages = db.get_messages_by_offer(offer_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this offer")
    return messages


@app.get("/{file_path:path}", response_class=FileResponse)
def get_file(file_path: str):
    full_path = Path("frontend") / file_path
    if full_path.is_file():
        return FileResponse(path=full_path)
    raise HTTPException(status_code=404, detail="File Not Found")
