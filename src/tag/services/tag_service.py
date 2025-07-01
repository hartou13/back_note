from fastapi import HTTPException
from src.tag.models.tag import Tag
from src.database.mysql_connector import get_db
from sqlalchemy import select
from src.tag.dto.tag import CreateTagDto

async def create_tag_service(tag: CreateTagDto, user_id: str):
    async with get_db() as db:
        existing_tag = await db.scalar(select(Tag).where(Tag.name == tag.name, Tag.user_id == user_id))
        if existing_tag:
            raise HTTPException(status_code=400, detail="Tag already exists")
        tag = Tag(name=tag.name, user_id=user_id, color=tag.color)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        return tag
    
async def get_tag_service(tag_id: str, user_id: str):
    async with get_db() as db:
        return await db.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))
    
async def get_all_tags(user_id: str):
    async with get_db() as db:
        return (await db.scalars(select(Tag).where(Tag.user_id == user_id))).all()
    
async def update_tag_service(tag: CreateTagDto, tag_id: str, user_id: str):
    async with get_db() as db:
        existing_tag = await db.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))
        if not existing_tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        existing_tag.name = tag.name
        existing_tag.color = tag.color
        await db.commit()
        await db.refresh(existing_tag)
        return existing_tag

async def get_tag_service(tag_id: str, user_id: str):
    async with get_db() as db:
        return await db.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))

async def delete_tag_service(tag_id: str, user_id: str):
    async with get_db() as db:
        tag = await db.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        await db.delete(tag)
        await db.commit()
        return tag
    
async def check_tag_ownership(tag_id: str, user_id: str):
    tag = await get_tag_service(tag_id, user_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
