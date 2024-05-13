from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime
from sqlalchemy.orm import Session
from app import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token, status_code=200)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db :Session = Depends(database.get_db)):

    print(user_credentials)
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #update last login date
    db.query(models.User).\
    filter(models.User.email == user_credentials.username).\
    update({'last_login': datetime.now()})
    db.commit()
    #create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"access_token":access_token, "token_type":"bearer"}

@router.post('/verify_token',status_code=200)
def verify_token( current_user: int = Depends(oauth2.get_current_user)):
    return {"role":"user","user_id":current_user.id}