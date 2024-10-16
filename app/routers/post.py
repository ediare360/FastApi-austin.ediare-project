from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from typing import Optional
from .. import models,utils,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from .. import models,schemas
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




@router.get('/', response_model=list[schemas.Post])
def get_post(db:Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user),limit:int=10,skip: int = 0,search:Optional[str]=''):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # count_query = db.query(func.count(models.Vote.post_id)).scalar()
    # count_query = db.query(func.count(models.Vote.post_id)).filter(models.Post.id == models.Vote.post_id).scalar() 
    # results = db.query(models.Post,func.count((models.Post.id)))\.join(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).all()
    # result = db.query(models.Post,models.Vote.post_id    ).join(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).all()
    # query = (db.query(models.Post,func.count(models.Vote.post_id).label('count_column_x').join(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id))        
    # query = (db.query(models.Post,func.count(models.Vote.post_id).label('count_column_x')  ).join(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id))
    
    return posts

  
    

        
        

     
   

    # if not posts:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"post with id:{id} does not exist")

    # cursor.execute('''select * from posts''')
    # posts= cursor.fetchall()
    # print(posts)
    


# @app.get("/posts")
# def read_root():
#     return {"Hello": my_posts}

# @app.post('/posts')
# def createpost(post:Post):
#     cursor.execute('''insert into posts(title,content,published) VALUES(%s,%s,%s) RETURNING * ''',(post.title, post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     # post_doc = post.model_dump()
#     # post_doc['id']= randrange(0,1000000000)
#     # my_posts.append(post_doc)
#     return{'postdate':new_post}


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    # new_post = post.model_dump()
    # print(**post.model_dump())
    # new_post =models.Post(title=post.title, content=post.content, published=post.published)
    # print("pleasedddddddddddddddddddddddddddddd")
    # print(user_id.id)
    
    new_post = models.Post(own_id= user_id.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{'data':posts}



# @app.get("/posts/latest")
# def get_latest_post():
#     post =  my_posts[len(my_posts)-1]
#     return {'detail': post}



@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int, db:Session= Depends(get_db)):
    # post = cursor.execute('''select * from posts where id=%s ''', (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"post with id:{id} does not exist")
    return post
       
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    # cursor.execute('''delete from posts where id =%s returning*''',(str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()


    # index = find_index_post(id)
    if post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"post with id:{id} does not exist")
    
    if post.own_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Not Authorized to perform this action")

    
    post.delete(synchronize_session=False)
    db.commit()
    return Response (status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@router.put("/{id}")
def update_post(id:int, update_post:schemas.PostBase, db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    # # index = find_index_post(id)
    # cursor.execute('''update posts SET title=%s, content=%s, published=%s where id =%s RETURNING*''',(post.title,post.content,post.published, str(id)))
    # update_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f'post with id:{id} does not exist')
    
    if post.own_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Not Authorized to perform this action")
    


    post_query.update(update_post.model_dump(),synchronize_session = False)
    db.commit()
    

    # post_dict = post.model_dump()
    # post_dict['id']=id

    # my_posts[index]= post_dict
    
    return post_query.first()

    # post_dict = post.model_dump()
    # print(post_dict)
      

    # for p in my_posts:
    #     if p['id'] == (int(id)):
    #         post_d = p
            
       
    #         return {'data':post_d} 



    