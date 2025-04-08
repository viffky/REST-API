from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    status = Column(String(20), default="todo")