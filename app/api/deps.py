from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.token import TokenData

# Définit le flow d'authentification OAuth2 avec route de génération de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible d'authentifier l'utilisateur",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """Dépendance FastAPI: retourne l'utilisateur courant validé par JWT."""
    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise _credentials_exception()
        token_data = TokenData(user_id=user_id)
    except Exception:
        raise _credentials_exception()

    user = await UserRepository(db).get_by_id(token_data.user_id)
    if user is None:
        raise _credentials_exception()
    return user
