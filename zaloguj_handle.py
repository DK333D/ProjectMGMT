from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext

import help

router: APIRouter = APIRouter()

# Secret key and token settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, help.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/zaloguj")
async def serve_login_form(request: Request):
    return help.get_template_no_query(request, "zaloguj.html")

@router.post("/zaloguj")
async def zaloguj(user: help.User, request: Request):
    email = user.email
    haslo = user.haslo
    is_user_verified = await help.verify_user(email, haslo)
    if not is_user_verified:
        raise HTTPException(status_code=401, detail="Invalid email or haslo")
    else:
        request.session["email"] = email

        is_admin = help.verify_user_is_admin(email)
        if(is_admin):
            request.session["isAdmin"] = is_admin
        return RedirectResponse(url="/dashboard")

@router.get("/wyloguj")
async def wyloguj(request: Request):
    session = request.session
    if "email" in session:
        del request.session["email"]

    if "isAdmin" in session:
        del request.session["isAdmin"]
    return RedirectResponse(url="/zaloguj")
