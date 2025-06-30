from fastapi import APIRouter, Depends

from src.note.services.note import get_notes_by_project_service
from src.project.dto.project import CreateProjectDto
from src.project.services.project_service import create_project_service, delete_project_service, get_project_service, get_projects_service, update_project_service
from src.users.services.user_service import find_user_service, get_current_user


router = APIRouter(
    prefix="/project",
    tags=["project"],
    responses={404: {"description": "Not found"}},
)

@router.post("")
async def create_project(project: CreateProjectDto, current_user: str = Depends(get_current_user)):
    project = await create_project_service(project, current_user)
    return project

@router.put("/{project_id}")
async def update_project(project_id: str, project: CreateProjectDto, current_user: str = Depends(get_current_user)):
    project = await update_project_service(project_id, project, current_user)
    return project

@router.get("/{project_id}")
async def get_project(project_id: str, current_user: str = Depends(get_current_user)):
    project = await get_project_service(project_id, current_user)
    return project

@router.get("")
async def get_projects(current_user: str = Depends(get_current_user)):
    projects = await get_projects_service(current_user)
    return projects

@router.delete("/{project_id}")
async def delete_project(project_id: str, current_user: str = Depends(get_current_user)):
    project = await delete_project_service(project_id, current_user)
    return project

@router.get("/{project_id}/notes")
async def get_notes_by_project(project_id: str, current_user: str = Depends(get_current_user)):
    notes = await get_notes_by_project_service(project_id, current_user)
    return notes

