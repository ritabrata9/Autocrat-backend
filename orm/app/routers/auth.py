# CONTAINS ROUTES FOR AUTH OPS SUCH AS LOGIN ETC

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.utils import verify_pwd


router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code=401, detail=f"Cant validate credentials", headers={"WWW-Authenticate": "Bearer"})

    user = db.query(models.User).filter(models.User.email == user_credentials.username.lower()).first()

    if not user:
        raise credentials_exception
    
    if not verify_pwd(user_credentials.password, user.password):
        raise credentials_exception
        
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "role": user.role}    
    )    

    return {"access_token": access_token, "token_type": "bearer"}





