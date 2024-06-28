from app import models, schemas, utils
from fastapi import FastAPI, Response, status,  HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/signup",
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED,response_model=schemas.UserOut) 
def create_user(user : schemas.UserCreate, db :Session = Depends(get_db)):

    # Check for existing user by username or email (adjust based on your uniqueness constraints)
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        # Customize the error message if desired (e.g., include which field conflicts)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this username or email already exists."
        )

    #hash the password - user.password 
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
