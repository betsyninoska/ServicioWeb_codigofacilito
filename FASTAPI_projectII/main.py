
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException

from pydantic import ValidationError
from schemas import UserRequestModel 
from database import User
from database import Movie
from database import UserReview
from database import database as connection
from schemas import UserResponseModel

from schemas import ReviewRequestModel
from schemas import ReviewResponseModel

app = FastAPI(title='Proyecto FASTAPI', Description= 'Proyecto para diseñar películas', version= '1.0')
 



@app.on_event("startup")
    



#@asynccontextmanager
#async def lifespan(app: FastAPI):

async def startup_event():

    print('El servidor va a comenzar')
    # Conectar a la base de datos
    connection.connect()
    # Crear tablas si no existen
    with connection:
        connection.create_tables([User, Movie, UserReview], safe=True)  # Asegúrate de incluir todas las tablas necesarias
   

    if not connection.is_closed():
        connection.close()  # Cerrar la conexión al finalizar




@app.get("/")
async def index():
     return 'Saludos desde el servidor FASTAPI'





@app.post("/users", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    # Überprüfen, ob der Benutzername bereits existiert
    #if User.select().where(User.username == user.username).exists():
    if User.select().where(User.username == user.username).first():
        raise HTTPException(status_code=409, detail='El username ya se encuentra en uso')

    # Passwort hashen
    hash_password = User.create_password(user.password)

    # Neuen Benutzer erstellen
    new_user = User.create(
        username=user.username, 
        password=hash_password
        )
    
    print(new_user)  # Debugging-Ausgabe

    #return {'id': new_user.id, 'username': new_user.username}
    #return UserResponseModel(id=new_user.id, username=new_user.username)
    #convertir un objeto de tipo model de peewe a diccionario para retornar
    return user


@app.post("/reviews", response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    try:
        
           user = User.get_by_id(user_review.user_id)
           movie = Movie.get_by_id(user_review.movie_id)

           
           user_review_instance = UserReview.create(
               user=user,
               movies=movie,
               review=user_review.review,
               score=user_review.score,
               create_at=datetime.now()
           )
           return user_review_instance
    except ValidationError as e:
        return {"error": str(e)}



@app.get("/about")
async def about():
    return "About"