from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from backend.db.crud import crud_test
from backend.db.db_core import get_db

router = APIRouter()


@router.post("/test_add")
def test_add(db: Session = Depends(get_db)):
    return crud_test.add(db)
