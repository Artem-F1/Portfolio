import uuid
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base



class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_completed: Mapped[bool | None]= mapped_column(Boolean, default=False)
    