from datetime import datetime
import uuid
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text, ForeignKey
from src.database.mysql_connector import Base

class Tag(Base):
    __tablename__ = "tags"
    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )    
    name = Column(String(255), index=True)
    user_id = Column(String(36))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    color = Column(String(7), server_default="#2973B2")



