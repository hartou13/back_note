from typing import List, Optional

from pydantic import BaseModel, Field

class CreateProjectDto(BaseModel):
    name: str = Field(..., description="The name field is required")
    description: str = Field(..., description="The description field is required")
    mother_project_id: Optional[str] = None
    color: Optional[str] = None