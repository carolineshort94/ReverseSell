from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from datetime import datetime

Base = declarative_base()


class DBAccount(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    contact_phone: Mapped[str] = mapped_column(nullable=False)
    registration_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_login: Mapped[Optional[datetime]] = mapped_column(default=None)
    profile_description: Mapped[Optional[str]] = mapped_column(default=None)
    profile_img: Mapped[Optional[str]] = mapped_column(default=None)
    session_token: Mapped[Optional[str]] = mapped_column(default=None)
    session_expires_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class DBRequest(Base):
    __tablename__ = "request"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    category_id: Mapped[int] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_range: Mapped[Optional[int]] = mapped_column(default=None)
    location: Mapped[str] = mapped_column(nullable=False)
    location_range: Mapped[Optional[str]] = mapped_column(nullable=True)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(default=None)
    status: Mapped[str] = mapped_column(default="open")
    post_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class DBCategory(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(default=None)


class DBOffer(Base):
    __tablename__ = "offer"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    request_id: Mapped[int] = mapped_column(index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    offer_description: Mapped[Optional[str]] = mapped_column(default=None)
    offer_price: Mapped[float] = mapped_column(nullable=False)
    offer_quantity: Mapped[int] = mapped_column(nullable=False)
    seller_location: Mapped[str] = mapped_column(nullable=False)
    delivery_time: Mapped[Optional[int]] = mapped_column(default=None)
    warranty: Mapped[Optional[str]] = mapped_column(default=None)
    offer_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[str] = mapped_column(default="pending")


class DBProduct_image(Base):
    __tablename__ = "product_image"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    offer_id: Mapped[int] = mapped_column(index=True)
    upload_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    image_url: Mapped[str] = mapped_column(nullable=False)
    order_index: Mapped[int] = mapped_column(nullable=False)


class DBMessage(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(index=True)
    receiver_id: Mapped[int] = mapped_column(index=True)
    offer_id: Mapped[int] = mapped_column(index=True)
    content: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(default=False)
