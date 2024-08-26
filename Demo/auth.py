# auth.py
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from Demo.db.db import get_db
from Demo.db.models.user_model import UsersModel
from Demo.db.repository.base import get_entity_by_filter

load_dotenv()

# Load secrets and configurations from .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer instance for token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(
        plain_password,
        hashed_password
):
    return pwd_context.verify(plain_password, hashed_password)


# Function to authenticate the user
def authenticate_user(
        session: Session,
        username: str,
        password: str
):
    user = get_entity_by_filter(session, UsersModel, [UsersModel.username == username])
    if not user:
        raise ValueError("User not found")

    if verify_password(password, user.hashed_password):
        return user
    raise ValueError("Incorrect password")



# Function to create an access token
def create_access_token(
        data: dict,
        expires_delta: timedelta = 5
):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Function to retrieve the current user
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UsersModel).filter(UsersModel.username == username).first()
    if user is None:
        raise credentials_exception
    return user

