from pydantic import BaseModel, Field
from typing import Optional


class TodoBase(BaseModel):
    """Schéma commun entre lecture/création des todos."""
    title: str = Field(..., min_length=1)
    description: Optional[str] = None


class TodoCreate(TodoBase):
    """Schéma de création de todo (hérite de TodoBase)."""
    pass


class TodoUpdate(BaseModel):
    """Schéma de mise à jour de todo. Tous les champs sont optionnels."""
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoRead(TodoBase):
    """Schéma de sortie pour un todo lu depuis la DB."""
    id: int
    completed: bool
    owner_id: int

    model_config = {
        "from_attributes": True
    }
