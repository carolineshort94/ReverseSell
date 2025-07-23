from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
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
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), index=True)
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
    request_id: Mapped[int] = mapped_column(ForeignKey("request.id"), index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), index=True)
    offer_description: Mapped[Optional[str]] = mapped_column(default=None)
    offer_price: Mapped[float] = mapped_column(nullable=False)
    offer_quantity: Mapped[int] = mapped_column(nullable=False)
    seller_location: Mapped[str] = mapped_column(nullable=False)
    product_link: Mapped[Optional[str]] = mapped_column(default=None)
    delivery_time: Mapped[Optional[int]] = mapped_column(default=None)
    warranty: Mapped[Optional[str]] = mapped_column(default=None)
    offer_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[str] = mapped_column(default="pending")


class DBProductImage(Base):  # Renamed for convention
    __tablename__ = "product_image"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offer.id"), index=True)
    upload_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    image_url: Mapped[str] = mapped_column(nullable=False)
    order_index: Mapped[int] = mapped_column(nullable=False)


class DBMessage(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("account.id"), index=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("account.id"), index=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offer.id"), index=True)
    content: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )  # Ensure not nullable
