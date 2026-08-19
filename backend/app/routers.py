from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import TaskSchema, TaskCreate, TaskUpdate
from app.services import TaskService
from typing import List
import uuid



router = APIRouter(
    prefix="/tasks",
    tags=['task']
)


@router.get('', response_model=List[TaskSchema],
    status_code=status.HTTP_200_OK)
async def get_tasks_router(db: AsyncSession = Depends(get_db)) -> List[TaskSchema]:
    service = TaskService(db)
    tasks = await service.get_all_tasks()
    return tasks
    
    
@router.post('',                                                                  response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED)
async def post_tasks_router(payload: TaskCreate,     db: AsyncSession = Depends(get_db)) -> TaskSchema:
    service = TaskService(db)
    new_task = await service.create_tasks(payload)
    return new_task
    

@router.patch('/{task_id}',
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK)
async def patch_tasks_router(task_id: uuid.UUID, data: TaskUpdate,
    db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    change_task = await service.update_tasks(task_id, data)
    if not change_task:
        raise HTTPException(status_code=404,
            detail="Not found")
    return change_task
    
    
@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_tasks_router(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
