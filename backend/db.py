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
    DBUsers,
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


def update_request(request_id: int) -> ResquestOut | None:
    db = SessionLocal()
    db_request = db.query(DBRequest).filter(DBRequest.id == request_id).first()
    if not db_request:
        db.close()
        return None

    # Update the request status or any other fields as needed
    db_request.status = "updated"  # Example update
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
