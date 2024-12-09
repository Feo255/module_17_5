from venv import create

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def get_all_tasks(db : Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")
async def get_task(db : Annotated[Session, Depends(get_db)], task_id: int):
    task_ = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    return task_

@router.post("/create")
async def create_task(db : Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   user_id=user_id,
                                   slug=slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'tansaction': 'Succesful'}



@router.put("/update")
async def update_task(db : Annotated[Session, Depends(get_db)], update_task: UpdateTask, task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    db.execute(update(Task).where(Task.id == task_id).values(title=create_task.title,
                                                            content=create_task.content,
                                                            priority=create_task.priority,
                                                             slug=slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'tansaction': 'Succesful'}


@router.delete("/delete")
async def delete_task(db : Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'tansaction': 'Succesful'}