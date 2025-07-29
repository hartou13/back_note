from enum import Enum
import uuid
from sqlalchemy import Boolean, Column, DateTime, SmallInteger, String, text, ForeignKey
from src.database.mysql_connector import Base
from sqlalchemy.orm import relationship


class TaskStatus(Enum):
    TODO = 0
    WAITING = 25
    IN_PROGRESS = 50
    DONE = 100

class Task(Base):
    __tablename__ = "tasks"
    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(255), index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    mother_task_id = Column(String(36), ForeignKey("tasks.id"))
    status = Column(SmallInteger, default=TaskStatus.TODO.value)
    priority = Column(SmallInteger, default=1)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    finished_at = Column(DateTime, nullable=True)
    mother_task = relationship("Task", 
        backref="daughters",
        remote_side=[id],
        foreign_keys=[mother_task_id])
    project = relationship("Project", backref="tasks")


