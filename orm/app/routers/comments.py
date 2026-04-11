from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, oauth2
from app.schemas import CommentIn
from fastapi import HTTPException, Depends, APIRouter, status
from app.models import Post, Comments

router = APIRouter(
    prefix="/comments", 
    tags=['Comments']
)

@router.get("/{id}", status_code=200)
def getComments(id: int, db: Session = Depends(get_db)):
    
    post_exists = db.query(Post.id).filter(Post.id == id).first() is not None
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    comments = db.query(models.Comments).options(
        joinedload(models.Comments.user)
    ).filter(models.Comments.post_id == id).all()
    return comments

@router.post("/{id}", status_code=201)
def createComment(id: int, comment: CommentIn, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
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

@router.delete("/{id}", status_code=204)
def deleteComment(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    query = db.query(models.Comments).filter(models.Comments.id == id)

    comment = query.first()
    if comment is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")
    
    query.delete(synchronize_session=False)
    db.commit()


    
    

