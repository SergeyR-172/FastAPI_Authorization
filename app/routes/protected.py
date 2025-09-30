from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import HTMLResponse

from authx import TokenPayload
from auth_config import security, bearer_scheme

router = APIRouter()


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