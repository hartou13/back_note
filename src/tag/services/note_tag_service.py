from fastapi import HTTPException
from src.note.services.note import check_note_ownership, get_note_service
from src.tag.models.note_tag import NoteTag
from src.database.mysql_connector import get_db
from sqlalchemy import select

from src.tag.services.tag_service import check_tag_ownership

async def tag_note_service(note_id: str, tag_id: str, user_id: str):
    async with get_db() as db:
        await check_note_ownership(note_id, user_id)
        await check_tag_ownership(tag_id, user_id)
        note_tag = await db.scalar(select(NoteTag).where(NoteTag.note_id == note_id, NoteTag.tag_id == tag_id))
        if note_tag:
            print("Note already tagged")
        else:
            note_tag = NoteTag(note_id=note_id, tag_id=tag_id)
            db.add(note_tag)
            await db.commit()
            await db.refresh(note_tag)
        return note_tag
    
async def untag_note_service(note_id: str, tag_id: str, user_id: str):
    async with get_db() as db:
        await check_note_ownership(note_id, user_id)
        await check_tag_ownership(tag_id, user_id)
        note_tag = await db.scalar(select(NoteTag).where(NoteTag.note_id == note_id, NoteTag.tag_id == tag_id))
        if not note_tag:
            raise HTTPException(status_code=404, detail="Note not tagged")
        await db.delete(note_tag)
        await db.commit()
        return note_tag

async def clear_note_tag_service(note_id: str, current_user_id:str):
    await check_note_ownership(note_id, current_user_id)
    async with get_db() as db:
        note_tags = await db.scalars(select(NoteTag).where(NoteTag.note_id == note_id))
        for note_tag in note_tags:
            await db.delete(note_tag)
        await db.commit()
        return note_tags

async def set_note_tags_service(note_id: str, tag_ids: list[str], current_user_id: str):
    await check_note_ownership(note_id, current_user_id)
    await clear_note_tag_service(note_id, current_user_id)
    for tag_id in tag_ids:
        await tag_note_service(note_id, tag_id, current_user_id)
    return await get_note_service(note_id, current_user_id)