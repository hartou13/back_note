from fastapi import APIRouter, Depends

from src.tag.dto.tag import CreateTagDto
from src.tag.services.tag_service import create_tag_service, delete_tag_service, get_all_tags, get_tag_service, update_tag_service
from src.users.services.user_service import get_current_user

router = APIRouter(
    prefix="/tag",
    tags=["tag"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def get_tags(current_user: str = Depends(get_current_user)):
    tags = await get_all_tags(current_user)
    return tags

@router.post("")
async def create_tag(tag: CreateTagDto, current_user: str = Depends(get_current_user)):
    tag = await create_tag_service(tag, current_user)
    return tag

@router.put("/{tag_id}")
async def update_tag(tag_id: str, tag: CreateTagDto, current_user: str = Depends(get_current_user)):
    tag = await update_tag_service(tag, tag_id, current_user)
    return tag

@router.delete("/{tag_id}")
async def delete_tag(tag_id: str, current_user: str = Depends(get_current_user)):
    tag = await delete_tag_service(tag_id, current_user)
    return tag

@router.get("/{tag_id}")
async def get_tag(tag_id: str, current_user: str = Depends(get_current_user)):
    tag = await get_tag_service(tag_id, current_user)
    return tag