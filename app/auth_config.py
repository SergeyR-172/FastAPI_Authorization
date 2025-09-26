from authx import AuthX, AuthXConfig
from fastapi.security import HTTPBearer

config = AuthXConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = AuthX(config=config)
bearer_scheme = HTTPBearer()
