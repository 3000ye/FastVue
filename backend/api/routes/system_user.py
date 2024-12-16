from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.crud import crud_system
from backend.db.schema.schema_system import AddUser, UpdateUser, DeleteUser, QueryUser
from backend.db.db_core import get_db

router = APIRouter()


@router.post("/add_user")
def add_user(item: AddUser, db: Session = Depends(get_db)):
    return crud_system.add_user(item=item, db=db)


@router.post("/update_user")
def update_user(item: UpdateUser, db: Session = Depends(get_db)):
    return crud_system.update_user(item=item, db=db)


@router.post("/delete_user")
def delete_user(item: DeleteUser, db: Session = Depends(get_db)):
    return crud_system.delete_user(item=item, db=db)


@router.post("/query_user")
def query_user(item: QueryUser, db: Session = Depends(get_db)):
    return crud_system.query_user(item=item, db=db)
