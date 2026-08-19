from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models import Task
from app.schemas import TaskSchema, TaskCreate, TaskUpdate
import uuid



class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_all(self) -> List[TaskSchema]:
        sessia = await self.db.execute(select(Task))
        return sessia.scalars().all()
        
    async def create_task(self, task_data: TaskCreate) -> Task:
        task_create = Task(title=task_data.title,is_completed=False)
        self.db.add(task_create)
        await self.db.commit()
        await self.db.refresh(task_create)
        return task_create
        
    async def update_task(self, task_id: uuid.UUID, task_up_data: TaskUpdate) -> Task | None:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task:
            return None
        update_data = task_up_data.model_dump(exclude_unset=True, by_alias=True)

        if 'completed' in update_data:
            update_data['is_completed'] = update_data.pop('completed')

        for key, val in update_data.items():
            setattr(task, key, val)
        await self.db.commit()
        await self.db.refresh(task)
        return task
        
        
    async def delete_task(self, data_id: uuid.UUID) -> None:
        response_del = await self.db.execute(select(Task).where(Task.id == data_id))
        task = response_del.scalar_one_or_none()
        if not task:
            return False
            
        await self.db.delete(task)
        await self.db.commit()
        return True