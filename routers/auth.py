from fastapi import Request, HTTPException, APIRouter, Response, Depends
from jose import jwt, JWTError
from app.config import settings
# from google.oauth2 import id_token
# from google.auth.transport import requests
# from datetime import datetime, timezone
import requests as req
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.User import User
from app.database import get_session as get_db
from schemas.user import UserPublic

router = APIRouter(
    prefix="/auth", tags=["auth"]
)

def create_jwt(user_data):
    return jwt.encode(user_data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def verify_jwt(request: Request, db: AsyncSession):
    print("Verifying JWT for request:", request.cookies.get("jwt"))
    # Extract Authorization Header
    token = request.cookies.get("jwt")
    if not token:
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    try:
        print("Verifying JWT token:", token)
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM], options={"verify_exp": True})
        # if payload.get("exp", '') < datetime.now(timezone.utc).timestamp():
        #     raise HTTPException(status_code=401, detail="Token expired")

        # Attach user info so handlers can use it
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await get_current_user(email=email, db=db)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        request.state.user = UserPublic.model_validate(user)
        print("Verified JWT payload:", payload)
        request.state.google_user_info = payload  
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def exchange_code_for_tokens(code: str) -> dict[str, str]: 
    """Exchange authorization code for access and ID tokens."""
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    print("Exchanging code for tokens with data:", data)

    response = req.post(token_url, data=data)
    response_json = response.json()
    print("Exchanged code for tokens:", response_json)
    return response_json

def get_google_userinfo(code: str):
    """Fetch user info from Google using access token."""
    tokens = exchange_code_for_tokens(code)
    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to obtain access token from Google")
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://openidconnect.googleapis.com/v1/userinfo"
    response = req.get(url, headers=headers)
    response_json = response.json()
    print("Fetched Google user info:", response_json)
    return response_json

async def get_or_create_user(db: AsyncSession, *, email: str, given_name: str = None, family_name: str = None, sub: str = None, picture: str = None, email_verified: bool = False, **kwargs) -> User:
    user = await get_current_user(email, db)

    if user:
        return user

    user = User(
        email=email,
        first_name=given_name,
        last_name=family_name,
        google_id=sub,
        avtar_url=picture,
        email_verified=email_verified
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_current_user(
    email: str,
    db: AsyncSession = Depends(get_db)
) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    return user

    
@router.post("/google/callback")
async def google_auth(data: dict, response: Response, db: AsyncSession = Depends(get_db)):
    """
    Receives Google ID token from frontend, verifies it, returns backend JWT.
    """
    print("Google auth callback called with data:", data)
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing Google Authorization Code")

    google_user_info = get_google_userinfo(code)
    await get_or_create_user(db=db, **google_user_info)
    jwt_token = create_jwt(google_user_info)
    response.set_cookie(
        key="jwt", 
        value=jwt_token, 
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=3600 * 24 * 7 # 1 week
        )

    return google_user_info

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("jwt")
    return {"status": "logged_out"}


@router.get("/validate-session")
async def validate_session(request: Request):
    return {"status": "valid", "google_user_info": request.state.google_user_info}