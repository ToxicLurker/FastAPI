from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    id: str
    first_name: str
    second_name: Union[str, None] = None
    age: Union[str, None] = None
    birthdate: Union[str, None] = None
    biography: Union[str, None] = None
    city: Union[str, None] = None
    disabled: Union[int, None] = None

class UserInDB(User):
    hashed_password: str