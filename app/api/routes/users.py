from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import register_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=UserRead)
async def register(user_create: UserCreate, db=Depends(get_db)):
    """Enregistrement d'un nouvel utilisateur. Expose UserRead en réponse."""
    user = await register_user(UserRepository(db), user_create)
    return user
