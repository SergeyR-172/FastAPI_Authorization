# app/init_db.py
from database import engine
from models.base import Base
from models.user import User  # Оставьте, если нужно (не обязательно для create_all)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)