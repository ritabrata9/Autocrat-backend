from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.services.upload_service import upload_profile_pic
from app.db.database import get_db
from app.db import models
from app.core.oauth2 import get_current_user
from app.schemas import UserCreate, UserOut, BioUpdate
from app.utils import hash_password

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

# * CREATE USER
@router.post("/", status_code=201, response_model = UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    #hash the password    
    user.password = hash_password(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)      
    db.commit()           
    db.refresh(new_user) 
    return new_user

# * GET /users/{id} — returns a single user info by id
@router.get("/{id}", response_model = UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()  # SELECT * FROM users WHERE id = %s
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user

# * DELETE USER
@router.delete("/{id}", status_code=204)
def del_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    if id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorised")
    
    db.delete(user)
    db.commit()


@router.patch("/updatebio/{id}", status_code=200, response_model=UserOut)
def update_bio(id: int, payload: BioUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    if id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorised")
    
    user.bio = payload.bio
    
    db.commit()
    db.refresh(user)

    return user


# * UPLOAD PROFILE PIC
@router.post("/profile-pic")
def upload_dp(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    image_url = upload_profile_pic(file.file, current_user.id)

    current_user.profile_picture_url = image_url
    db.commit()

    return {"url": image_url}

@router.patch("/profile-pic")
def delete_profile_pic(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
       
    if id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorised")
    

    current_user.profile_picture_url = None

    db.commit()

    return current_user

    

        
