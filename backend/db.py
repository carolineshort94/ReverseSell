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
from schemas import RequestOut, RequestCreate, OfferCreate, OfferOut
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


def create_offer(data: OfferCreate) -> OfferOut:
    db = SessionLocal()
    new_offer = DBOffer(**data.dict())
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    result = OfferOut.from_orm(new_offer)
    db.close()
    return result


def get_offers_by_request(request_id: int) -> list[OfferOut]:
    db = SessionLocal()
    db_offers = db.query(DBOffer).filter(DBOffer.request_id == request_id).all()
    offers = [OfferOut.from_orm(offer) for offer in db_offers]
    db.close()
    return offers


def update_offer(offer_id: int, data: OfferCreate) -> OfferOut:
    db = SessionLocal()
    offer_to_update = db.query(DBOffer).filter(DBOffer.id == offer_id).first()
    if not offer_to_update:
        db.close()
        raise ValueError("Offer not found")

    for key, value in data.dict().items():
        setattr(offer_to_update, key, value)

    db.commit()
    db.refresh(offer_to_update)
    result = OfferOut.from_orm(offer_to_update)
    db.close()
    return result
