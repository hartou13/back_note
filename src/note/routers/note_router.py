from typing import List
from fastapi import APIRouter, Depends, Query

from src.note.dto.note import CreateNoteDto
from src.note.services.note import create_note_service, delete_note_service, get_note_service, get_notes_by_project_service, get_notes_service, update_note_service, search_notes_service
from src.project.dto.project import CreateProjectDto
from src.project.services.project_service import create_project_service, delete_project_service, get_project_service, get_projects_service, update_project_service
from src.users.services.user_service import find_user_service, get_current_user
from src.tag.services.note_tag_service import tag_note_service, untag_note_service


router = APIRouter(
    prefix="/note",
    tags=["note"],
    responses={404: {"description": "Not found"}},
)

@router.post("")
async def create_note(note: CreateNoteDto, current_user: str = Depends(get_current_user)):
    note = await create_note_service(note, current_user)
    return note

@router.put("/{note_id}")
async def update_note(note_id: str, note: CreateNoteDto, current_user: str = Depends(get_current_user)):
    note = await update_note_service(note_id, note, current_user)
    return note

@router.post("/{note_id}/tag/{tag_id}")
async def tag_note(note_id: str, tag_id: str, current_user: str = Depends(get_current_user)):
    note_tag = await tag_note_service(note_id, tag_id, current_user)
    return note_tag

@router.delete("/{note_id}/tag/{tag_id}")
async def untag_note(note_id: str, tag_id: str, current_user: str = Depends(get_current_user)):
    note_tag = await untag_note_service(note_id, tag_id, current_user)
    return note_tag

@router.get("/{note_id}")
async def get_note(note_id: str, current_user: str = Depends(get_current_user)):
    note = await get_note_service(note_id, current_user)
    return note

@router.get("")
async def get_notes(
    page: int = Query(None, description="Numéro de page"),
    page_size: int = Query(10, description="Taille de la page"),
    query: str = Query("", description="Terme de recherche"),
    project_id: str = Query(None, description="ID du projet"),
    tag_ids: List[str] = Query(None, description="Liste des IDs de tags"),
    current_user: str = Depends(get_current_user)
):
    if page is not None:
        notes = await search_notes_service(query, current_user, page=page, page_size=page_size, project_id=project_id, tag_ids=tag_ids or [])
    else:
        notes = await get_notes_service(current_user)
    return notes

@router.delete("/{note_id}")
async def delete_note(note_id: str, current_user: str = Depends(get_current_user)):
    note = await delete_note_service(note_id, current_user)
    return note