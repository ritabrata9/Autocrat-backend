from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.schemas import CommentIn
from fastapi import HTTPException, Depends, APIRouter, status
from app.models import Post

router = APIRouter(
    prefix="/comments", 
    tags=['Comments']
)

@router.post("/{id}", status_code=201)
def create_comment(id: int, comment: CommentIn, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    post_exists = db.query(Post.id).filter(Post.id == id).first() is not None
    if  not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    new_comment = models.Comments(
    post_id=id,
    user_id=current_user.id,
    content=comment.content
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

    
    

