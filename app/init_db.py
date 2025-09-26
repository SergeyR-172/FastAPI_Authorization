from database import engine
from models.base import Base
from models.user import User

if __name__ == "__main__":
    print("Инициализация базы данных")
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы")
    except Exception as e:
        print("Ошибка инициализации")
    print("Инициализация базы данных завершена")