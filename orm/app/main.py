from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import post, user, auth, likes
import time
from sqlalchemy.exc import OperationalError



# creates all tables defined in models.py if they don't already exist
# equivalent to running the CREATE TABLE sql manually in the raw version
for _ in range(10):
    try:
        models.Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        time.sleep(2)
        
app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/debug/db")
def debug_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        url = str(db.bind.url)  # shows which DB you're actually connected to
        tables = db.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname='public'"
        )).fetchall()
        return {
            "connected_to": url,
            "tables": [t[0] for t in tables]
        }
    except Exception as e:
        return {"error": str(e)}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)

    
