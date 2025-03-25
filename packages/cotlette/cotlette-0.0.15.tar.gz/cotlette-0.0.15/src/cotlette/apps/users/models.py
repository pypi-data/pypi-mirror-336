# from cotlette.db import models

from pydantic import BaseModel
from cotlette.models import Model
from cotlette.fields import CharField, IntegerField

# Pydantic-модель для создания нового пользователя
class UserCreate(BaseModel):
    name: str
    age: int

# Pydantic-модель для представления пользователя
class User(BaseModel):
    id: int
    name: str
    age: int

# Определение модели пользователя через ORM
class UserModel(Model):
    name = CharField(max_length=50)
    age = IntegerField()