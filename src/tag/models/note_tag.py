from datetime import datetime
import uuid
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text, ForeignKey
from src.database.mysql_connector import Base
from sqlalchemy.orm import relationship

class NoteTag(Base):
    __tablename__ = "note_tags"
    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )    
    note_id = Column(String(36), ForeignKey("notes.id", ondelete="CASCADE"))
    tag_id = Column(String(36), ForeignKey("tags.id", ondelete="CASCADE"))
    note = relationship("Note", backref="tags")
    tag = relationship("Tag", backref="notes")


