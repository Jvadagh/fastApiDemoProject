# authentication_service.py
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from Demo.auth import authenticate_user
from Demo.auth import create_access_token


def check_credentials(form_data: OAuth2PasswordRequestForm, db: Session):
    return authenticate_user(db, form_data.username, form_data.password)


def generate_login_token(user):
    access_token_expires = timedelta(minutes=2)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires}
