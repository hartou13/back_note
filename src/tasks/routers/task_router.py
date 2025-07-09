from fastapi import APIRouter, Depends

from src.tasks.dto.task_dto import CreateTaskDto, UpdateTaskDto
from src.tasks.services.task_service import create_task_service, delete_task_service, get_main_tasks_service, get_task_service, get_tasks_service, update_task_service
from src.users.services.user_service import get_current_user

router = APIRouter(
    prefix="/task",
    tags=["task"],
    responses={404: {"description": "Not found"}},
)

@router.post("")
async def create_task(task: CreateTaskDto, current_user: str = Depends(get_current_user)):
    task = await create_task_service(task, current_user)
    return task

@router.get("")
async def get_tasks(current_user: str = Depends(get_current_user)):
    tasks = await get_main_tasks_service(current_user)
    return tasks

@router.put("/{task_id}")
async def update_task(task_id: str, task: UpdateTaskDto, current_user: str = Depends(get_current_user)):
    task = await update_task_service(task_id, task, current_user)
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: str, current_user: str = Depends(get_current_user)):
    task = await delete_task_service(task_id, current_user)
    
@router.get("/{task_id}")
async def get_task(task_id: str, current_user: str = Depends(get_current_user)):
    task = await get_task_service(task_id, current_user)
    return task