from venv import create

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def get_all_users(db : Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/user_id")
async def get_user(db : Annotated[Session, Depends(get_db)], user_id: int):
    user_ = db.scalars(select(User).where(User.id == user_id)).first()
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    return user_

@router.get("/user_id/tasks")
async def get_user(db : Annotated[Session, Depends(get_db)], user_id: int):
    user_ = db.scalars(select(User).where(User.id == user_id))
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks

@router.post("/create")
async def create_user(db : Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'tansaction': 'Succesful'}


@router.put("/update")
async def update_user(db : Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    db.execute(update(User).where(User.id == user_id).values(firstname=update_user.firstname,
                                                            lastname=update_user.lastname,
                                                            age=update_user.age,
                                                            ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'tansaction': 'Succesful'}


@router.delete("/delete")
async def delete_user(db : Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'tansaction': 'Succesful'}