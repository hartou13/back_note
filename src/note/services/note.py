from typing import List
from fastapi import HTTPException
from src.project.models.project import Project
from src.database.mysql_connector import get_db
from src.note.dto.note import CreateNoteDto
from src.note.models.note import Note
from sqlalchemy import select, delete, func, or_
from sqlalchemy.orm import joinedload, load_only

from src.tag.models.note_tag import NoteTag

async def create_note_service(note: CreateNoteDto, user_id: str):
    from src.tag.services.note_tag_service import set_note_tags_service
    async with get_db() as db:
        existing_note = await db.scalar(select(Note).where(Note.title == note.title, Note.user_id == user_id))
        if existing_note:
            raise HTTPException(status_code=400, detail="Note already exists")
        new_note = Note(
            title=note.title,
            content=note.content,
            user_id=user_id,
            project_id=note.project_id,
            hidden=note.hidden,
        )
        db.add(new_note)
        await db.commit()
        await db.refresh(new_note)
        if note.tags:
            await set_note_tags_service(new_note.id, note.tags, user_id)
        return new_note
    
async def update_note_service(note_id: str, note: CreateNoteDto, user_id: str):
    from src.tag.services.note_tag_service import set_note_tags_service
    async with get_db() as db:
        existing_note = await db.scalar(select(Note).where(Note.id == note_id, Note.user_id == user_id))
        if not existing_note:
            raise HTTPException(status_code=404, detail="Note not found")
        existing_note.title = note.title
        existing_note.content = note.content
        existing_note.project_id = note.project_id
        existing_note.hidden = note.hidden
        await db.commit()
        await db.refresh(existing_note)
        if note.tags:
            await set_note_tags_service(note_id, note.tags, user_id)
        return existing_note

async def delete_note_service(note_id: str, user_id: str):
    async with get_db() as db:
        note = await db.scalar(select(Note).where(Note.id == note_id, Note.user_id == user_id))
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        await db.execute(delete(Note).where(Note.id == note_id))
        await db.commit()
        return note
    
async def get_note_service(note_id: str, user_id: str):
    async with get_db() as db:
        note = await db.scalar(select(Note).where(Note.id == note_id, Note.user_id == user_id))
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    
async def get_notes_service(user_id: str):
    async with get_db() as db:
        notes = await db.scalars(select(Note).options(
            joinedload(Note.project).options(load_only(Project.id, Project.name, Project.color)),
            joinedload(Note.tags).joinedload(NoteTag.tag)
        ).where(Note.user_id == user_id).order_by(Note.created_at.desc()))
        return notes.unique().all()
    
async def search_notes_service(query: str, user_id: str, page: int=0, page_size: int=10, project_id: str=None, tag_ids: List[str]=[]):
    async with get_db() as db:
        filters = [Note.user_id == user_id]
        if query:
            filters.append(or_(Note.title.ilike(f"%{query}%"), Note.content.ilike(f"%{query}%")))
        if project_id:
            filters.append(Note.project_id == project_id)
        if tag_ids:
            filters.append(Note.tags.any(NoteTag.tag_id.in_(tag_ids)))
        notes = await db.scalars(select(Note).options(
            joinedload(Note.project).options(load_only(Project.id, Project.name, Project.color)),
            joinedload(Note.tags).joinedload(NoteTag.tag)
        ).where(*filters).order_by(Note.created_at.desc()).limit(page_size).offset(page * page_size))
        notes = notes.unique().all()
        count = await db.scalar(select(func.count()).select_from(Note).where(*filters))
        return {
            "data": notes,
            "pagination": {
                "total": count,
                "page": page,
                "pageSize": page_size
            }
        }
    # 695000
async def get_notes_by_project_service(project_id: str, user_id: str):
    async with get_db() as db:
        notes = await db.scalars(select(Note).where(Note.project_id == project_id, Note.user_id == user_id))
        return notes.all()
    
async def check_note_ownership(note_id: str, user_id: str):
    note = await get_note_service(note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
