from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate
from passlib.hash import pbkdf2_sha256
from typing import Optional


hash = pbkdf2_sha256.hash("password")

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user