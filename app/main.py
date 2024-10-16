from fastapi import FastAPI, Response,status,HTTPException,Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from.import models,utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from . import models,schemas
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware







# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["https://www.google.com/","https://www.google.com/"]


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Connect to an existing database

# while True:
#     try:
#         conn = psycopg2.connect(host ='localhost', database = 'fastapi',user ='postgres', password='Manjecta4sky',cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("connection is established !!!!!!!")
#         break
    
#     except Exception as error:
#         print('No connection was established')
#         print('Error :', error)
    


my_posts = [{'title':'title of post 1','content':'content of post 1','id':1},
            {'title':'title of post 2','content':'content of post 2','id':2},
            {'title':'title of post 3','content':'content of post 3','id':3}]


def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
        


