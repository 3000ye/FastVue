from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import jwt

from db.crud import crud_system
from db.model.db_system import SystemUser
from db.db_core import get_db
from core.system_auth import verify_password, create_access_token, decode_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/system_auth/token")


def _current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        data = decode_access_token(token)
        return crud_system.query_by_username(data["username"], db)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


def current_user(user: SystemUser = Depends(_current_user)):
    if user.status != 1:
        raise HTTPException(status_code=400, detail=f"user [{user.username}] have been disabled")

    return user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: SystemUser = crud_system.query_by_username(form_data.username, db)
    flag = verify_password(form_data.password, user.password)

    if flag:
        expires = timedelta(hours=24)
        access_token = create_access_token({"username": user.username}, expires_delta=expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

