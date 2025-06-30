from fastapi import HTTPException
from src.database.mysql_connector import get_db
from src.project.models.project import Project
from src.project.dto.project import CreateProjectDto
from sqlalchemy import select

async def create_project_service(project: CreateProjectDto, user_id: str):
    async with get_db() as db:
        existing_project = await db.scalar(select(Project).where(Project.name == project.name, Project.user_id == user_id))
        if existing_project:
            raise HTTPException(status_code=400, detail="Project already exists")
        project = Project(
            name=project.name,
            description=project.description,
            mother_project_id=project.mother_project_id,
            user_id=user_id,
            color=project.color,
        )
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project
    
async def update_project_service(project_id: str, project: CreateProjectDto, user_id: str):
    async with get_db() as db:
        existing_project = await db.scalar(select(Project).where(Project.id == project_id, Project.user_id == user_id))
        if not existing_project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.name:
            existing_project.name = project.name
        if project.description:
            existing_project.description = project.description
        if project.mother_project_id:
            if len(project.mother_project_id.strip()) != 36:
                existing_project.mother_project_id = None
            else:
                existing_project.mother_project_id = project.mother_project_id
        if project.color:
            existing_project.color = project.color
        await db.commit()
        await db.refresh(existing_project)
        return existing_project
    
async def get_project_service(project_id: str, user_id: str):
    async with get_db() as db:
        project = await db.scalar(select(Project).where(Project.id == project_id, Project.user_id == user_id))
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    
async def get_projects_service(user_id: str):
    async with get_db() as db:
        projects = await db.scalars(select(Project).where(Project.user_id == user_id))
        return projects.all()
    
async def delete_project_service(project_id: str, user_id: str):
    async with get_db() as db:
        project = await db.scalar(select(Project).where(Project.id == project_id, Project.user_id == user_id))
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        await db.delete(project)
        await db.commit()
        return project