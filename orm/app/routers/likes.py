from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.schemas import VoteResponse
from fastapi import HTTPException, Depends, APIRouter


router = APIRouter(
    prefix = "/vote",
    tags = ['Likes']
)

# ! LIKE
@router.post("/{id}", status_code=201, response_model=VoteResponse)
def like(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
   
   # check if already liked
    existing_vote = db.query(models.Votes).filter(
        models.Votes.post_id == id,
        models.Votes.user_id == current_user.id
    ).first()

    if existing_vote:
        raise HTTPException(status_code=409, detail="Already liked")

    new_vote = models.Votes(
        post_id=id,
        user_id=current_user.id
    )
    
    db.add(new_vote) 

    # increment like_count
    db.query(models.Post).filter(models.Post.id == id).update(
        {models.Post.like_count: models.Post.like_count + 1},
        synchronize_session=False
    )  

    db.commit()          
    db.refresh(new_vote) 
    return new_vote


# ! UNLIKE
@router.delete("/{id}", status_code=204)
def unlike(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    query = db.query(models.Votes).filter(
        models.Votes.post_id == id,
        models.Votes.user_id == current_user.id
    )

    vote = query.first()

    if vote is None:
        raise HTTPException(status_code=404, detail=f"Vote with id {id} not found")
    
    if vote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    query.delete(synchronize_session=False)

    # decrement like_count
    db.query(models.Post).filter(models.Post.id == id).update(
        {models.Post.like_count: models.Post.like_count - 1},
        synchronize_session=False
    )
    db.commit()
