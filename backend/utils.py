import bcrypt
from secrets import token_urlsafe
from datetime import datetime, timedelta
from .models import DBAccount
from .db import SessionLocal
from typing import Optional
from .schemas import UserPublicDetails

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
        if not account or not verify_password(password, account.password_hash):
            return None

        session_token = token_urlsafe()
        now = datetime.utcnow()
        account.session_token = session_token
        account.session_expires_at = now + timedelta(minutes=SESSION_LIFE_MINUTES)
        account.last_login = now
        db.commit()
        return session_token


def validate_session(email: str, session_token: str) -> bool:
    with SessionLocal() as db:
        account = db.query(DBAccount).filter(DBAccount.email == email).first()
        if not account or account.session_token != session_token:
            return False
        if (
            not account.session_expires_at
            or datetime.utcnow() >= account.session_expires_at
        ):
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

        details = UserPublicDetails(
            email=account.email,
            first_name=account.first_name,
            last_name=account.last_name,
            contact_phone=account.contact_phone,
            registration_date=account.registration_date,
            profile_description=account.profile_description,
            profile_img=account.profile_img,
        )

        # actually invalidate
        account.session_token = None
        account.session_expires_at = None
        db.commit()
        return details


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
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode(
        "utf-8"
    )


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    try:
        if not hashed.startswith("$2"):
            return False
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False
