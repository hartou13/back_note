from typing import Optional
from pydantic import BaseModel, Field

from src.tasks.models.task import TaskStatus

class CreateTaskDto(BaseModel):
    name: str = Field(..., description="The name field is required")
    description: str = Field(..., description="The description field is required")
    project_id: str = Field(..., description="The project_id field is required")
    mother_task_id: Optional[str] = Field(None, description="The mother_task_id field is required")
    # status: TaskStatus = Field(..., description="The status field is required")
    priority: Optional[int] = Field(None, description="The priority field is required")
    
class UpdateTaskDto(BaseModel):
    name: Optional[str] = Field(None, description="The name field is required")
    description: Optional[str] = Field(None, description="The description field is required")
    project_id: Optional[str] = Field(None, description="The project_id field is required")
    mother_task_id: Optional[str] = Field(None, description="The mother_task_id field is required")
    status: Optional[TaskStatus] = Field(None, description="The status field is required")
    priority: Optional[int] = Field(None, description="The priority field is required")