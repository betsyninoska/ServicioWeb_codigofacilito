import hashlib
from peewee import *
from datetime import datetime


database = MySQLDatabase('fastapi_project2', 
                         user='root', 
                         password='123456', 
                         host='localhost', 
                         port=3306)


def __str__(self):
        return self.username




class User(Model):
        id = AutoField()  # Autoincrementales ID-Feld
        username=CharField(max_length=50,unique=True)
        password= CharField(max_length=50)
        create_at=DateTimeField(default=datetime.now)
        def __str__(self):
                return self.username
        class Meta:
                database =database
                table_name = 'users'
        @classmethod
        def create_password(cls,password):
                h= hashlib.md5()
                h.update(password.encode('utf-8'))
                return h.hexdigest()

class Movie(Model):
        title=CharField(max_length=50)
        create_at=DateTimeField(default=datetime.now)
        def __str__(self):
                return self.titlele
        class Meta:
                database=database
                table_name = 'movies'

class UserReview(Model):                   
        user=ForeignKeyField(User, backref='reviews')
        movies=ForeignKeyField(Movie, backref='reviews')
        score=TextField()
        create_at=DateTimeField(default=datetime.now)
        def __str__(self):
                return f'{self.user.username} - {self.movie.title}'
        class Meta:
                database=database
                table_name = 'UserReview'



