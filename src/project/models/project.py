from datetime import datetime
import uuid
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text, ForeignKey
from src.database.mysql_connector import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )    
    name = Column(String(255), index=True)
    description = Column(String(255))
    user_id = Column(String(36))
    mother_project_id = Column(String(36), ForeignKey("projects.id"), nullable = True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    color = Column(String(7), server_default="#2973B2")


