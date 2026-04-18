from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import cloudinary.uploader
from app.db.database import get_db
from app.db.models import User, Post
from app.core.oauth2 import get_current_user

router = APIRouter()

@router.post("/users/profile-pic")
def upload_profile_pic(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Validate type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 2. Upload to Cloudinary
    result = cloudinary.uploader.upload(
        file.file,
        folder="profile_pics",
        public_id=f"user_{current_user.id}",
        overwrite=True
    )

    image_url = result["secure_url"]

    image_url = image_url.replace(
    "/upload/",
    "/upload/w_200,h_200,c_fill,q_auto,f_auto/"
)

    # 3. Save in DB
    current_user.profile_picture_url = image_url
    db.commit()

    return {"url": image_url}

@router.patch("/users/profile-pic")
def delete_profile_pic(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
       
    if id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorised")
    

    current_user.profile_picture_url = None

    db.commit()

    return current_user