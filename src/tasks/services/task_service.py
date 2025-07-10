from datetime import datetime, timedelta
from fastapi import HTTPException
from src.project.models.project import Project
from src.database.mysql_connector import get_db
from src.tasks.models.task import Task, TaskStatus
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload, load_only

from src.tasks.dto.task_dto import CreateTaskDto, UpdateTaskDto

async def create_task_service(task_dto: CreateTaskDto, user_id: str):
    async with get_db() as db:
        existing_task = await db.scalar(select(Task).where(Task.name == task_dto.name, Task.user_id == user_id, Task.project_id == task_dto.project_id))
        if existing_task:
            raise HTTPException(status_code=400, detail="Task already exists")
        if task_dto.mother_task_id:
            mother_task = await db.scalar(select(Task).where(Task.id == task_dto.mother_task_id, Task.user_id == user_id))
            if not mother_task:
                raise HTTPException(status_code=404, detail="Mother task not found")
            if mother_task.project_id != task_dto.project_id:
                raise HTTPException(status_code=400, detail="Mother task and task project do not match")
            if mother_task.status == TaskStatus.DONE:
                mother_task.status = TaskStatus.TODO
        task = Task(
            name=task_dto.name,
            description=task_dto.description,
            user_id=user_id,
            project_id=task_dto.project_id,
            mother_task_id=task_dto.mother_task_id,
            priority=task_dto.priority
        )
        db.add(task)
        await db.commit()
        task = await db.scalar(select(Task).options(
            joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color)),
            # joinedload(Task.daughters).options(joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color)))
        ).where(Task.id == task.id))
        return task

async def get_task_service(task_id: str, user_id: str):
    async with get_db() as db:
        task = await db.scalar(select(Task).options(
            joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color)),
            joinedload(Task.daughters).options(joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color)))
        ).where(Task.id == task_id, Task.user_id == user_id))
        return task
    
async def get_tasks_service(user_id: str):
    async with get_db() as db:
        tasks = await db.scalars(select(Task).options(
            joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color))
        ).where(Task.user_id == user_id).order_by(Task.created_at.desc()))
        return tasks.unique().all()
    
async def get_main_tasks_service(user_id: str):
    async with get_db() as db:
        tasks = await db.scalars(select(Task).options(
            joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color))
        ).where(
            Task.user_id == user_id, Task.mother_task_id == None,
            or_(
                Task.status != TaskStatus.DONE.value,
                Task.created_at > datetime.now() - timedelta(days=14)
            )
        ).order_by(Task.created_at.desc()))
        return tasks.unique().all()
    
async def update_task_service(task_id: str, task_dto: UpdateTaskDto, user_id: str):
    async with get_db() as db:
        existing_task = await db.scalar(select(Task).options(
            joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color)),
            # joinedload(Task.daughters).options(joinedload(Task.project).options(load_only(Project.id, Project.name, Project.color)))
        ).where(Task.id == task_id, Task.user_id == user_id))
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task_dto.name:
            existing_task.name = task_dto.name
        if task_dto.description:
            existing_task.description = task_dto.description
        if task_dto.mother_task_id:
            mother_task = await db.scalar(select(Task).where(Task.id == task_dto.mother_task_id, Task.user_id == user_id))
            if not mother_task:
                raise HTTPException(status_code=404, detail="Mother task not found")
            if mother_task.project_id != existing_task.project_id:
                raise HTTPException(status_code=400, detail="Mother task and task project do not match")
            existing_task.mother_task_id = task_dto.mother_task_id
        if task_dto.project_id:
            if existing_task.project_id != task_dto.project_id:
                await propagate_project_id_to_daughters(task_id, task_dto.project_id)
            existing_task.project_id = task_dto.project_id
        if task_dto.status:
            if task_dto.status == TaskStatus.DONE:
                await propagate_status_to_daughters(task_id, task_dto.status)
            existing_task.status = task_dto.status.value
        if task_dto.priority:
            existing_task.priority = task_dto.priority
        await db.commit()
        return existing_task
    
async def delete_task_service(task_id: str, user_id: str):
    async with get_db() as db:
        task = await db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await db.delete(task)
        await db.commit()
        
async def propagate_project_id_to_daughters(task_id: str, new_project_id: str):
    async with get_db() as db:
        daughters = await db.scalars(select(Task).where(Task.mother_task_id == task_id))
        for daughter in daughters:
            daughter.project_id = new_project_id
            await propagate_project_id_to_daughters(daughter.id, new_project_id)
        await db.commit()
        
async def propagate_status_to_daughters(task_id: str, new_status: TaskStatus):
    async with get_db() as db:
        daughters = await db.scalars(select(Task).where(Task.mother_task_id == task_id))
        for daughter in daughters:
            daughter.status = new_status.value
            await propagate_status_to_daughters(daughter.id, new_status)
        await db.commit()

#TODO: tags
#TODO: due dates