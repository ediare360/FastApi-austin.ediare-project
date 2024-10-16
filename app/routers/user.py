from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from .. import models,utils
from ..database import engine,get_db
from sqlalchemy.orm import Session
from .. import models,schemas


router = APIRouter(
    prefix="/users",
    tags=['User']
)



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserPres)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hash_password = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
