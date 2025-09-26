from fastapi import FastAPI
from routes import user as user_routes
from auth_config import security, bearer_scheme
import uvicorn

app = FastAPI()

app.include_router(user_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")