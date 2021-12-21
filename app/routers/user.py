from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#######################
######## Users ########
#######################

#### Create 1 ####
@router.post("/", status_code=status.HTTP_201_CREATED ,response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = models.User(**user.dict())
        hashed_pw = utils.hash(user.password)
        new_user.password = hashed_pw
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exists")
    return new_user

#### Read 1 ####
@router.get("/{id}",response_model=schemas.UserCreateResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"User with id {id} was not found")
    return user
