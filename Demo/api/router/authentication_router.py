# authentication_router.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from Demo.db.db import get_db
from Demo.db.services.authentication_service import generate_login_token, check_credentials

authentication_router = APIRouter()



# Token endpoint for user login
@authentication_router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    try:
        user = check_credentials(form_data, db)
        return generate_login_token(user)
    except NoResultFound:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    except ValueError as error:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

