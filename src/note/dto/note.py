from typing import List, Optional

from pydantic import BaseModel, Field

class CreateNoteDto(BaseModel):
    title: str = Field(..., description="The title field is required")
    content: str = Field(..., description="The content field is required")
    project_id: str = Field(..., description="The project_id field is required")
    tags: Optional[List[str]] = Field([], description="The tags field is required")