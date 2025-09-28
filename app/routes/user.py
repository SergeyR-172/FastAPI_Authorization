from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from schemas.user import UserCreate, UserOut, UserLogin
from crud.user import create_user, get_user_by_username
from authx import TokenPayload
from passlib.hash import pbkdf2_sha256
from auth_config import security, bearer_scheme

router = APIRouter()


@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
    summary="Регистрация нового пользователя",
    description="Создаёт нового пользователя с уникальным именем и паролем.",
    tags=["Authentication"],
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
    tags=["Authentication"],
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


@router.get(
    "/me",
    summary="Получить профиль текущего пользователя",
    description="Возвращает информацию о текущем авторизованном пользователе.",
    tags=["Users"],
    responses={
        200: {"description": "Профиль пользователя успешно получен"},
        401: {"description": "Неавторизованный доступ"}
    }
)
async def get_profile(
    payload: TokenPayload = Depends(security.access_token_required),
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    return {
        "id": payload.sub,
        "admin": getattr(payload, "admin", False)
    }


@router.get(
    "/protected",
    summary="Доступ к защищённому ресурсу",
    description="Эндпоинт доступен только при наличии действительного токена доступа.",
    tags=["Protected"],
    responses={
        200: {"description": "Доступ разрешён"},
        401: {"description": "Неавторизованный доступ"}
    },
    dependencies=[Depends(security.access_token_required), Security(bearer_scheme)]
)
async def get_protected():
    return HTMLResponse("Защищённая страница")


async def require_admin(payload: TokenPayload = Depends(security.access_token_required)):
    if not getattr(payload, "admin", False):
        raise HTTPException(status_code=403, detail="Требуются права администратора")
    return payload


@router.get(
    "/admin-protected",
    summary="Доступ только для администраторов",
    description="Эндпоинт доступен только пользователям с правами администратора.",
    tags=["Admin"],
    responses={
        200: {"description": "Доступ для администратора разрешён"},
        403: {"description": "Доступ запрещён — только для администраторов"},
        401: {"description": "Неавторизованный доступ"}
    },
    dependencies=[Depends(require_admin), Security(bearer_scheme)]
)
async def get_admin_protected():
    return HTMLResponse("Страница только для администраторов")
