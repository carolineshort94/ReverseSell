from pydantic import BaseModel, Field
from typing import Optional


# schema for user registration request
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    user_type: str = "buyer"  # default to 'buyer' if not specified


# schema for user login request
class UserLogin(BaseModel):
    email: str
    password: str


# schema for the token response (after successful login/registration)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# schema for a user's profile stored in Firestore
class UserProfile(BaseModel):
    uid: str  # firestore user id
    email: str
    first_name: str
    last_name: str
    user_type: str
    registration_date: str
    last_login: str
    profile_description: Optional[str]
