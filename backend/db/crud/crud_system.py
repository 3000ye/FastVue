from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.model.db_system import SystemUser
from core.system_auth import hash_password
from db.schema.schema_system import AddUser, UpdateUser, DeleteUser, QueryUser


def add_user(item: AddUser, db: Session):
    """
    新增用户，admin 使用，非注册入口
    """

    if len(item.username) > 32 or len(item.password) > 32:
        raise HTTPException(status_code=500, detail='Username or Password must be less than 32 characters')

    item.password = hash_password(item.password)
    _add = item.model_dump()
    print(_add)
    try:
        db.add(SystemUser(**_add))
        db.commit()
        return {"code": 0, "msg": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_user(item: DeleteUser, db: Session):
    """
    逻辑删除、注销用户
    """

    q = db.query(SystemUser).filter(SystemUser.id == item.id)
    flag = q.first()

    if flag:
        try:
            q.update({"status": 0})
            db.commit()
            return {"code": 0, "msg": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail='User not found')


def query_by_username(username: str, db: Session) -> SystemUser:
    """
    使用用户名查询用户，用于登录、权限校验
    """

    user = db.query(SystemUser).filter(SystemUser.username == username).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail='User not found')


def query_users(item: QueryUser, db: Session):
    """
    查询现有用户
    """

    q = db.query(
        SystemUser.id, SystemUser.username, SystemUser.email, SystemUser.status
    )

    if item.username:
        q = q.filter(SystemUser.username.like(f"%{item.username}%"))
    if item.email:
        q = q.filter(SystemUser.email.like(f"%{item.email}%"))
    if item.status:
        q = q.filter(SystemUser.status == item.status)

    return q.all()


def update_user(item: UpdateUser, db: Session):
    """
    更新用户信息
    """

    q = db.query(SystemUser).filter(SystemUser.id == item.id)
    flag = q.first()

    if flag:
        try:
            _update = item.model_dump()
            _update = dict(filter(lambda x: x[1] is not None, _update.items()))

            q.update(_update)
            db.commit()
            return {"code": 0, "msg": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail='User not found')
