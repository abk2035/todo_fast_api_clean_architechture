from datetime import timedelta

from app.core.config import settings
from app.core.exceptions import FunctionalError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.token import TokenData
from app.schemas.user import UserCreate


async def register_user(repo: UserRepository, user_create: UserCreate):
    """Inscritun utilisateur après vérification d'unicité de l'email."""
    existing = await repo.get_by_email(user_create.email)
    if existing:
        raise FunctionalError("Un utilisateur avec cet e-mail existe déjà", status_code=400)

    hashed_password = get_password_hash(user_create.password)
    return await repo.create(user_create=user_create, hashed_password=hashed_password)


async def authenticate_user(repo: UserRepository, email: str, password: str):
    user = await repo.get_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        raise FunctionalError("E-mail ou mot de passe incorrect", status_code=401)
    if not user.is_active:
        raise FunctionalError("Compte utilisateur inactif", status_code=403)
    return user


def create_token_for_user(user_id: int):
    to_encode = {"user_id": user_id}
    expire_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=to_encode, expires_delta=expire_delta)
    return {"access_token": access_token, "token_type": "bearer"}
