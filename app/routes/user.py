from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas.user import UserCreate, UserOut, UserLogin
from crud.user import create_user, get_user_by_username
from authx import TokenPayload

from passlib.hash import pbkdf2_sha256
from auth_config import security, bearer_scheme

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if not db_user or not pbkdf2_sha256.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = security.create_access_token(
        uid=db_user.username,
        data={"admin": db_user.is_admin}
    )
    return {"access_token": token}

@router.get('/me')
def get_profile(
    payload: TokenPayload = Depends(security.access_token_required),
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    return {
        "id": payload.sub,
        "admin": getattr(payload, "admin", False)
    }

@router.get("/protected", dependencies=[Depends(security.access_token_required), Security(bearer_scheme)])
def get_protected():
    return HTMLResponse("Protected page")

def require_admin(payload: TokenPayload = Depends(security.access_token_required)):
    if not getattr(payload, "admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

@router.get("/admin-protected", dependencies=[Depends(require_admin), Security(bearer_scheme)])
def get_admin_protected():
    return HTMLResponse("Admin protected page")
