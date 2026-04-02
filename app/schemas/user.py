from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Schéma partagé pour les informations de base de l'utilisateur."""
    email: EmailStr


class UserCreate(UserBase):
    """Schéma pour l'inscription utilisateur. Mot de passe sécurisé."""
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    """Schéma de lecture utilisateur retourné dans les réponses."""
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }
