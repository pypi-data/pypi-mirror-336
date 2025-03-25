from fastapi import APIRouter

from .models import User, UserModel, UserCreate


router = APIRouter()


# Создание таблицы при запуске приложения
@router.on_event("startup")
def create_tables():
    UserModel.create_table()

# Создание нового пользователя (POST)
@router.post("/users/", response_model=User)
def create_user(user: UserCreate):
    new_user = UserModel.objects.create(
        name=user.name,
        age=user.age
    )
    return {"id": 1, "name": new_user.name, "age": new_user.age}

# Получение всех пользователей (GET)
@router.get("/users/", response_model=None)
def get_users():
    users = UserModel.objects.all()
    return list(users)
