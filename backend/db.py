from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from secrets import token_urlsafe
from datetime import datetime
from models import (
    DBRequest,
    DBCategory,
    DBOffer,
    DBProduct_image,
    DBMessage,
    DBAccount,
    Base,
)
from schemas import ResquestOut
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def get_request(user_id: int) -> list[ResquestOut]:
    db = SessionLocal()
    db_requests = db.query(DBRequest).filter(DBRequest.user_id == user_id).all()
    request = []
    for db_request in db_requests:
        request.append(
            {
                "id": db_request.id,
                "user_id": db_request.user_id,
                "category_id": db_request.category_id,
                "title": db_request.title,
                "description": db_request.description,
                "quantity": db_request.quantity,
                "price_range": db_request.price_range,
                "location": db_request.location,
                "location_range": db_request.location_range,
                "expiry_date": db_request.expiry_date,
                "status": db_request.status,
                "post_date": db_request.post_date,
            }
        )
    db.close()
    return request


def update_request(
    request_id: int,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    quantity: int | None = None,
    price_range: int | None = None,
    location: str | None = None,
    location_range: str | None = None,
    expiry_date: datetime | None = None,
) -> ResquestOut | None:
    db = SessionLocal()
    db_request = db.query(DBRequest).filter(DBRequest.id == request_id).first()

    # Update the request status or any other fields as needed
    if status is not None:
        db_request.status = status
    if title is not None:
        db_request.title = title
    if description is not None:
        db_request.description = description
    if quantity is not None:
        db_request.quantity = quantity
    if price_range is not None:
        db_request.price_range = price_range
    if location is not None:
        db_request.location = location
    if location_range is not None:
        db_request.location_range = location_range
    if expiry_date is not None:
        db_request.expiry_date = expiry_date
    db.commit()

    updated_request = ResquestOut(
        id=db_request.id,
        user_id=db_request.user_id,
        category_id=db_request.category_id,
        title=db_request.title,
        description=db_request.description,
        quantity=db_request.quantity,
        price_range=db_request.price_range,
        location=db_request.location,
        location_range=db_request.location_range,
        expiry_date=db_request.expiry_date,
        status=db_request.status,
        post_date=db_request.post_date,
    )

    db.close()
    return updated_request
