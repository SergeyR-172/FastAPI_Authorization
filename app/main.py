from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from authx import AuthX, AuthXConfig, TokenPayload
import uvicorn

app = FastAPI()

config = AuthXConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = AuthX(config=config)
bearer_scheme = HTTPBearer()

@app.get("/login")
def login(username: str, password: str):
    if username == "user" and password == "pass":
        token = security.create_access_token(uid=username, data={"admin" : True})
        return {"access_token": token}
    raise HTTPException(401, detail={"message": "Invalid credentials"})

@app.get('/me')
def get_profile(
    payload: TokenPayload = Depends(security.access_token_required),
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    print(payload.model_dump())
    return {"id": payload.sub, "admin": getattr(payload, "admin", False)}

@app.get("/protected", dependencies=[Depends(security.access_token_required), Security(bearer_scheme)])
def get_protected():
    return HTMLResponse("Protected page")

def require_admin(payload: TokenPayload = Depends(security.access_token_required)):
    if not getattr(payload, "admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

@app.get("/admin-protected", dependencies=[Depends(require_admin), Security(bearer_scheme)])
def get_adminprotected():
    return HTMLResponse("Admin protected page")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")