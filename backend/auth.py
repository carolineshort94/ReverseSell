from fastapi import APIRouter, HTTPException, Request, Depends
from schemas import (
    SignupCredentials,
    LoginCredentials,
    SucessResponse,
    UserPublicDetails,
    SecretResponse,
)
from utils import (
    create_user_account,
    validate_email_password,
    validate_session,
    invalidate_session,
    get_user_public_details,
)

auth_router = APIRouter()


def get_auth_user(request: Request):
    email = request.session.get("email")
    token = request.session.get("session_token")
    if not email or not token:
        raise HTTPException(status_code=401)
    if not validate_session(email, token):
        raise HTTPException(status_code=403)
    return True


@auth_router.post("/sigup", response_model=SucessResponse)
async def sigup(credentials: SignupCredentials, request: Request):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    created = create_user_account(
        email=credentials.email,
        password=credentials.password,
        first_name=credentials.first_name,
        last_name=credentials.last_name,
        contact_phone=credentials.contact_phone,
    )
    if not created:
        raise HTTPException(status_code=409, detail="Email already exists")

    # Auto login after sigup
    token = validate_email_password(credentials.email, credentials.password)
    request.session["email"] = credentials.email
    request.session["session_token"] = token
    return SucessResponse(success=True)


@auth_router.post("/login", response_model=SucessResponse)
async def login(credentials: LoginCredentials, request: Request):
    token = validate_email_password(credentials.email, credentials.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    request.session["email"] = credentials.email
    request.session["session_token"] = token
    return SucessResponse(success=True)


@auth_router.get("/logout", response_model=SucessResponse)
async def logout(request: Request):
    email = request.session.get("email")
    token = request.session.get("session_token")
    if email and token:
        invalidate_session(email, token)
        request.session.clear()
        return SucessResponse(success=True)
    return SucessResponse(success=False)


@auth_router.get(
    "/me", response_model=UserPublicDetails, dependencies=[Depends(get_auth_user)]
)
async def me(request: Request):
    email = request.session.get("email")
    user = get_user_public_details(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


@auth_router.get(
    "/secret", response_model=SecretResponse, dependencies=[Depends(get_auth_user)]
)
async def secret():
    return SecretResponse(secret="you are authenticated")
