import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.schemas import TaskCreate, TaskSchema, TaskUpdate
from app.repositories import TaskRepository
from app.kash import RedisCache
from app.config import settings



class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)
        self.cache = RedisCache(settings.redis_url, settings.cache_ttl_seconds)
        
    async def get_all_tasks(self) -> List[Task]:
        cached_task = await self.cache.get(settings.cache_tasks_key)
        if cached_task is not None:
            return cached_task
        tasks = await self.task_repo.get_all()
        tasks_data = [
            {"id": str(t.id), "title": t.title, "completed": t.is_completed}
            for t in tasks
        ]
        await self.cache.set(settings.cache_tasks_key, tasks_data)
        return tasks_data
        
    async def create_tasks(self, task: TaskCreate) -> Task:
        create = await self.task_repo.create_task(task)
        await self.cache.delete(settings.cache_tasks_key)
        return create
        
    async def update_tasks(self, task_id: uuid.UUID, task_data: TaskUpdate) -> Task | None:
        up_task = await self.task_repo.update_task(task_id, task_data)
        if up_task:
            await self.cache.delete(settings.cache_tasks_key)
        return up_task
        
        
    async def delete_task(self, task_id: uuid.UUID) -> None:
        completed_del = await self.task_repo.delete_task(task_id)
        if completed_del:
            await self.cache.delete(settings.cache_tasks_key)
        return completed_del