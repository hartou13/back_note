from pydantic import BaseModel, Field

class CreateTagDto(BaseModel):
    name: str = Field(..., description="The name field is required")
    color: str = Field(..., description="The color field is required")