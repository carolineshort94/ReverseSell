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
from schemas import RequestOut, RequestCreate
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def get_all_requests() -> list[RequestOut]:
    db = SessionLocal()
    db_requests = db.query(DBRequest).all()
    requests = [RequestOut.from_orm(req) for req in db_requests]
    db.close()
    return requests


def get_request(user_id: int) -> list[RequestOut]:
    db = SessionLocal()
    db_requests = db.query(DBRequest).filter(DBRequest.user_id == user_id).all()
    requests = [RequestOut.from_orm(req) for req in db_requests]
    db.close()
    return requests


def create_request(data: RequestCreate) -> RequestOut:
    db = SessionLocal()
    new_request = DBRequest(**data.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    result = RequestOut.from_orm(new_request)
    db.close()
    return result


def update_request(request_id: int, data: RequestCreate) -> RequestOut:
    db = SessionLocal()
    request_to_update = db.query(DBRequest).filter(DBRequest.id == request_id).first()
    if not request_to_update:
        db.close()
        raise ValueError("Request not found")

    for key, value in data.dict().items():
        setattr(request_to_update, key, value)

    db.commit()
    db.refresh(request_to_update)
    result = RequestOut.from_orm(request_to_update)
    db.close()
    return result


def delete_request(request_id: int) -> bool:
    db = SessionLocal()
    request_to_delete = db.query(DBRequest).filter(DBRequest.id == request_id).first()
    if not request_to_delete:
        db.close()
        return False
    db.delete(request_to_delete)
    db.commit()
    db.close()
    return True
