from fastapi import FastAPI, Request
from routes import user as user_routes
from fastapi.responses import JSONResponse
from authx.exceptions import MissingTokenError
import uvicorn

app = FastAPI()

@app.exception_handler(MissingTokenError)
def missing_token_exception_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )


app.include_router(user_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")