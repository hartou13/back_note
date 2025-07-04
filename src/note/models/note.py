from datetime import datetime
import uuid
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text, ForeignKey, Text
from src.database.mysql_connector import Base
from sqlalchemy.orm import relationship

class Note(Base):
    __tablename__ = "notes"
    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )    
    title = Column(String(255))
    content = Column(Text)
    user_id = Column(String(36))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    hidden = Column(Boolean, default=False)
    project = relationship("Project", backref="notes")


