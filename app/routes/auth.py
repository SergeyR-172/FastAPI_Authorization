from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from schemas.user import UserCreate, UserOut, UserLogin
from crud.user import create_user, get_user_by_username
from passlib.hash import pbkdf2_sha256
from auth_config import security

router = APIRouter(tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
    summary="Регистрация нового пользователя",
    description="Создаёт нового пользователя с уникальным именем и паролем.",
    responses={
        201: {"description": "Пользователь успешно зарегистрирован"},
        400: {"description": "Имя пользователя уже существует"}
    }
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
    return await create_user(db, user)


@router.post(
    "/login",
    summary="Вход в систему",
    description="Аутентифицирует пользователя и возвращает JWT токен доступа.",
    responses={
        200: {"description": "Успешная аутентификация"},
        401: {"description": "Неверное имя пользователя или пароль"}
    }
)
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_db)):
    db_user = await get_user_by_username(db, user.username)
    if not db_user or not pbkdf2_sha256.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    token = security.create_access_token(
        uid=db_user.username,
        data={"admin": db_user.is_admin}
    )
    return {"access_token": token}