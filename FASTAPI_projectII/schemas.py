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


class ResponseModel(BaseModel):
    class Config:
            orm_mode = True
            getter_Dict = PeeweeGetterDict

#--------User ---------------

class UserRequestModel(BaseModel):
    username: str
    password: str
    @field_validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50 :
            raise ValueError('La longitud debe encontrarse  entre 3 y 50 carácteres ')
        return username

# Modelo Pydantic para la respuesta del usuario
class UserResponseModel(ResponseModel):
    id: int
    username: str
    


 #--------- Review ---------------   
class ReviewRequestModel(BaseModel):
     user_id: int
     movie_id: int
     review: str
     score :int

class ReviewResponseModel(ResponseModel):
    id: int
    review: str
    score:int