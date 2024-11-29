from sqlalchemy.orm import Session
from backend.db.model.db_test import Test


def add(db: Session):
    test_dict = {
        "username": "test003", "email": "test@test.com"
    }

    db.add(Test(**test_dict))
    db.commit()

    return {"code": 0, "msg": "OK"}
