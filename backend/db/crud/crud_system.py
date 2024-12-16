from sqlalchemy.orm import Session, query
from backend.db.model.db_system import SystemUser
from backend.db.schema.schema_system import AddUser, UpdateUser, DeleteUser, QueryUser


def add_user(item: AddUser, db: Session):
    _add = item.model_dump()
    print(_add)
    try:
        db.add(SystemUser(**_add))
        db.commit()
        return {"code": 0, "msg": "success"}
    except Exception as e:
        return {"code": -1, "msg": str(e)}


def update_user(item: UpdateUser, db: Session):
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
            return {"code": -1, "msg": str(e)}
    else:
        return {"code": -1, "msg": "user not found"}


def delete_user(item: DeleteUser, db: Session):
    q = db.query(SystemUser).filter(SystemUser.id == item.id)
    flag = q.first()

    if flag:
        try:
            q.update({"status": 0})
            db.commit()
            return {"code": 0, "msg": "success"}
        except Exception as e:
            return {"code": -1, "msg": str(e)}
    else:
        return {"code": -1, "msg": "user not found"}


def query_user(item: QueryUser, db: Session):
    q = db.query(SystemUser)

    if item.username:
        q = q.filter(SystemUser.username.like(f"%{item.username}%"))
    if item.email:
        q = q.filter(SystemUser.email.like(f"%{item.email}%"))
    if item.status:
        q = q.filter(SystemUser.status == item.status)

    return q.all()
