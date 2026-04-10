from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2
from app.schemas import PostCreate, PostResponse
from typing import List, Optional
from fastapi import HTTPException, Depends, APIRouter