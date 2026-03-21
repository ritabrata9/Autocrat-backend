from dotenv import load_dotenv
from pathlib import Path
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.schemas import TokenData
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# # load credentials from .env file
# load_dotenv(dotenv_path=Path('.') / '.env')


# os.getenv('DATABASE_USERNAME')



# SECRET_KEY
# algo = hs256
# expiration time

# generate using command:= openssl rand -hex 32    (bash)
SECRET_KEY = "62bc94dd8c55da1738cfc40b8c32bffce6707d70ad5d680e7b42560cffa71380"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)
        id: str = payload.get("user_id")
        print("ID:", id)
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError as e:
        print("JWT ERROR:", e)
        raise credentials_exception
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(status_code=401, detail=f"Cant validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
