from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from authx import TokenPayload
from auth_config import security, bearer_scheme

router = APIRouter(tags=["Users"])


@router.get(
    "/me",
    summary="Получить профиль текущего пользователя",
    description="Возвращает информацию о текущем авторизованном пользователе.",
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