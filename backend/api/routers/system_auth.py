from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import jwt

from db.crud import crud_system
from db.model.db_system import SystemUser as SystemUser
from db.db_core import get_db
from core.system_auth import verify_password, create_access_token, decode_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/system_auth/token")


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    使用 oauth2 进行登录表单验证，登录之后 24 小时之内有效
    """

    user: SystemUser = crud_system.query_by_username(form_data.username, db)
    flag = verify_password(form_data.password, user.password)

    if flag:
        expires = timedelta(hours=24)
        access_token = create_access_token({"username": user.username}, expires_delta=expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})


def _current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    返回当前登录的用户信息
    """

    try:
        data = decode_access_token(token)
        return crud_system.query_by_username(data["username"], db)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


@router.post("/current_user")
def current_user(user: SystemUser = Depends(_current_user)):
    if user.status != 1:
        raise HTTPException(status_code=400, detail=f"user [{user.username}] have been disabled")

    return user


def check_user(user: SystemUser = Depends(current_user)):
    """校验用户权限（页面）"""

    pass
