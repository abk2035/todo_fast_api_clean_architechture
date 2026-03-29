from pydantic import BaseModel


class Token(BaseModel):
    """Schéma de réponse du endpoint d'authentification."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schéma intermédaire pour la payload JWT décodée."""
    user_id: int | None = None
