from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id         = Column(Integer, primary_key=True, nullable=False)
    title      = Column(String, nullable=False)
    content    = Column(String, nullable=False)
    published  = Column(Boolean, server_default='TRUE', nullable=False)

    # TIMESTAMP with timezone=True stores UTC time; server_default=text('now()') lets postgres set it automatically
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    like_count = Column(Integer, nullable=False, server_default="0")

    user = relationship("User")


class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, nullable=False)
    email    = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    role     = Column(String, nullable=False, server_default="USER")  # USER / ADMIN

class Votes(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User")


    
