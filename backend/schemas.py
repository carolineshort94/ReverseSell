from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, date


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str


class SignupCredentials(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    contact_phone: str


class SucessResponse(BaseModel):
    success: bool


class SecretResponse(BaseModel):
    secret: str


class UserPublicDetails(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    contact_phone: str
    registration_date: datetime
    profile_description: Optional[str] = None
    profile_img: Optional[str] = None


class RequestCreate(BaseModel):
    user_id: int
    category_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price_range: Optional[int] = None
    location: str = Field(..., min_length=1)
    location_range: Optional[str] = None
    expiry_date: Optional[datetime] = None
    status: Optional[str] = "open"
    post_date: Optional[date] = date.today()

    class Config:
        orm_mode = True


class RequestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    quantity: Optional[int] = Field(None, gt=0)
    price_range: Optional[int] = None
    location: Optional[str] = Field(None, min_length=1)
    location_range: Optional[str] = None
    expiry_date: Optional[datetime] = None
    status: Optional[str] = None


class RequestOut(RequestCreate):
    id: int
    user_id: int
    category_id: int
    price_range: Optional[int] = None
    location_range: Optional[str] = None
    expiry_date: Optional[datetime] = None
    post_date: datetime
    status: Optional[str] = None

    class Config:
        orm_mode = True


class OfferCreate(BaseModel):
    request_id: int
    user_id: int
    offer_description: Optional[str] = None
    offer_price: Optional[float] = None
    offer_quantity: Optional[int] = None
    seller_location: Optional[str] = None
    product_link = Optional[str] = None
    delivery_date: Optional[datetime] = None
    warranty: Optional[str] = None
    offer_date: Optional[date] = date.today()
    status: Optional[str] = "pending"

    class Config:
        orm_mode = True


class OfferOut(OfferCreate):
    id: int


class ProductImageCreate(BaseModel):
    offer_id: int
    image_url: str = Field(..., min_length=1)
    order_index: int = Field(..., ge=0)


class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    offer_id: int
    content: str = Field(..., min_length=1)


class MessageUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)


class MessageOut(MessageCreate):
    id: int
    timestamp: datetime
    is_read: bool = False
