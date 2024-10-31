from pydantic import field_validator
from pydantic import ValidationError
from pydantic import BaseModel

from typing import Any

from peewee import ModelSelect
from pydantic.utils import GetterDict

#convertir nuestro objeto en un diccionario
class PeeweeGetterDict(GetterDict):

    def get(self, key:Any, default: Any = None):
        res=getattr(self._obj, key, default)
        if isinstance(res,ModelSelect):
            return list(res)
        return res


class UserRequestModel(BaseModel):
    username: str
    password: str
    @field_validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50 :
            raise ValueError('La longitud debe encontrarse  entre 3 y 50 carácteres ')
        return username
        
# Modelo Pydantic para la respuesta del usuario
class UserResponseModel(BaseModel):
    id: int
    username:str
    class Config:
            orm_mode = True
            getter_Dict = PeeweeGetterDict

