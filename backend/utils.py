import bcrypt
from secrets import token_urlsafe
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import DBAccount
from db import SessionLocal
from typing import Optional
from schemas import UserPublicDetails

SESSION_LIFE_MINUTES = 120


def create_user_account(
    email: str, password: str, first_name: str, last_name: str, contact_phone: str
) -> bool:
    with SessionLocal() as db:
        if db.query(DBAccount).filter(DBAccount.email == email).first():
            return False
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        account = DBAccount(
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            contact_phone=contact_phone,
        )
        db.add(account)
        db.commit()
        return True


def validate_email_password(email: str, password: str) -> Optional[str]:
    with SessionLocal() as db:
        account = db.query(DBAccount).filter(DBAccount.email == email).first()
        if not account:
            return None
        if not bcrypt.checkpw(password.encode(), account.password_hash.encode()):
            return None
        session_token = token_urlsafe()
        account.session_token = session_token
        account.session_expires_at = datetime.utcnow() + timedelta(
            minutes=SESSION_LIFE_MINUTES
        )
        account.last_login = datetime.utcnow()
        db.commit()
        return session_token


def validate_session(email: str, session_token: str) -> bool:
    with SessionLocal() as db:
        account = (
            db.query(DBAccount)
            .filter(DBAccount.email == email, DBAccount.session_token == session_token)
            .first()
        )
        if datetime.utcnow() >= account.session_expires_at:
            return False
        account.session_expires_at = datetime.utcnow() + timedelta(
            minutes=SESSION_LIFE_MINUTES
        )
        db.commit()
        return True


def invalidate_session(email: str) -> Optional[UserPublicDetails]:
    with SessionLocal() as db:
        account = db.query(DBAccount).filter(DBAccount.email == email).first()
        if not account:
            return None
        return UserPublicDetails(
            email=account.email,
            first_name=account.first_name,
            last_name=account.last_name,
            contact_phone=account.contact_phone,
            registration_date=account.registration_date,
            profile_description=account.profile_description,
            profile_img=account.profile_img,
        )


def get_user_public_details(email: str) -> Optional[UserPublicDetails]:
    with SessionLocal() as db:
        account = db.query(DBAccount).filter(DBAccount.email == email).first()
        if not account:
            return None
        return UserPublicDetails(
            email=account.email,
            first_name=account.first_name,
            last_name=account.last_name,
            contact_phone=account.contact_phone,
            registration_date=account.registration_date,
            profile_description=account.profile_description,
            profile_img=account.profile_img,
        )


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False
