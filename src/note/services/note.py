from fastapi import HTTPException
from src.database.mysql_connector import get_db
from src.note.dto.note import CreateNoteDto
from src.note.models.note import Note
from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def create_note_service(note: CreateNoteDto, user_id: str):
    async with get_db() as db:
        existing_note = await db.scalar(select(Note).where(Note.title == note.title, Note.user_id == user_id))
        if existing_note:
            raise HTTPException(status_code=400, detail="Note already exists")
        note = Note(
            title=note.title,
            content=note.content,
            user_id=user_id,
            project_id=note.project_id,
        )
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note
    
async def update_note_service(note_id: str, note: CreateNoteDto, user_id: str):
    async with get_db() as db:
        existing_note = await db.scalar(select(Note).where(Note.id == note_id, Note.user_id == user_id))
        if not existing_note:
            raise HTTPException(status_code=404, detail="Note not found")
        existing_note.title = note.title
        existing_note.content = note.content
        existing_note.project_id = note.project_id
        await db.commit()
        await db.refresh(existing_note)
        return existing_note

async def delete_note_service(note_id: str, user_id: str):
    async with get_db() as db:
        note = await db.scalar(select(Note).where(Note.id == note_id, Note.user_id == user_id))
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        await db.delete(note)
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
        notes = await db.scalars(select(Note).options(joinedload(Note.project)).where(Note.user_id == user_id).order_by(Note.created_at.desc()))
        return notes.all()
    
async def get_notes_by_project_service(project_id: str, user_id: str):
    async with get_db() as db:
        notes = await db.scalars(select(Note).where(Note.project_id == project_id, Note.user_id == user_id))
        return notes.all()