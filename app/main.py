from fastapi import FastAPI, Request
from routes import auth as auth_routes
from routes import users as user_routes
from routes import protected as protected_routes
from fastapi.responses import JSONResponse
from authx.exceptions import MissingTokenError
import uvicorn

app = FastAPI()

@app.exception_handler(MissingTokenError)
async def missing_token_exception_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )


app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(protected_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")