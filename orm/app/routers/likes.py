from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.schemas import VoteResponse

router = APIRouter(
    prefix="/vote",
    tags=['Likes']
)

# ! GET MY LIKES
@router.get("/me", response_model=List[int])
def get_my_likes(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # Query the database for just the post_id column where the user matches
    votes = db.query(models.Votes.post_id).filter(models.Votes.user_id == current_user.id).all()
    
    # Unpack it into a flat list of integers: [1, 5, 12]
    return [vote[0] for vote in votes]


# ! LIKE
@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=VoteResponse)
def like(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # 1. SECURITY FIX: Check if the post actually exists before liking it!
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    # 2. Check if already liked
    existing_vote = db.query(models.Votes).filter(
        models.Votes.post_id == id,
        models.Votes.user_id == current_user.id
    ).first()

    if existing_vote:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already liked")

    # 3. Create the vote
    new_vote = models.Votes(
        post_id=id,
        user_id=current_user.id
    )
    db.add(new_vote) 

    # 4. Increment like_count on the post
    db.query(models.Post).filter(models.Post.id == id).update(
        {models.Post.like_count: models.Post.like_count + 1},
        synchronize_session=False
    )  

    db.commit()          
    db.refresh(new_vote) 
    return new_vote


# ! UNLIKE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def unlike(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    query = db.query(models.Votes).filter(
        models.Votes.post_id == id,
        models.Votes.user_id == current_user.id
    )

    vote = query.first()

    if vote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote with id {id} not found")
    
    # (CLEANUP: Removed the redundant user check here, as the query above already handles it)

    query.delete(synchronize_session=False)

    # decrement like_count
    db.query(models.Post).filter(models.Post.id == id).update(
        {models.Post.like_count: models.Post.like_count - 1},
        synchronize_session=False
    )
    db.commit()