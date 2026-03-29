from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    """Modèle utilisateur SQLAlchemy."""
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(180), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relation un-à-plusieurs vers les todos
    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    """Modèle TODO SQLAlchemy."""
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    owner = relationship("User", back_populates="todos")
