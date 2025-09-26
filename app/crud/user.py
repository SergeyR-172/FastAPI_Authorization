from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from passlib.hash import pbkdf2_sha256
from typing import Optional


hash = pbkdf2_sha256.hash("password")

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user