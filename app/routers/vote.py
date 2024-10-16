from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from ..import database,schemas,models,utils,oauth2
from sqlalchemy.orm import Session
from ..database import engine,get_db



router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(get_db), user_id:int=Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id ==user_id.id)
    vote_query2 = db.query(models.Vote).filter(models.Vote.post_id == models.Vote.user_id ==user_id.id).first()
    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {user_id.id} has already voted {vote.post_id}")
        
        # if not found_vote:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Post does not exist {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = user_id.id )
        db.add(new_vote)
        db.commit()
        return{"Message":"Successfully added vote"}
    
    else:
           
        if  vote_query2.user_id != user_id.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Not Authorized to perform this action")
        
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post was ID: {vote.post_id} was not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"Message":"Successlly delete vote"}



    print(vote.model_dump())
    print('------------------------')
    print(vote)
 
    # print(vote.post_id)

    return {"Vote":"Thanks for your Vote"}