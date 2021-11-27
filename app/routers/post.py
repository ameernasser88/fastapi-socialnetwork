from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.sql.functions import current_user

from .. import models, schemas, utils, oath2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#######################
######## Posts ########
#######################

#### Read * ####
@router.get("/" , response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db),current_user=Depends(oath2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    # posts = db.query(models.Post).all()
    return posts

#### Read 1 ####
@router.get("/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {id} was not found")
    return post

#### Create 1 ####
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oath2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#### Delete 1 ####
@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="your are unauthorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#### Update 1 ####
@router.put("/{id}")
async def update_post(post: schemas.PostUpdate,id: int, db: Session = Depends(get_db), current_user=Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="your are unauthorized to perform requested action")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()