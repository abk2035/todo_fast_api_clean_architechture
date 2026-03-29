from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import authenticate_user, create_token_for_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """Route de connexion pour générer un token JWT."""
    user = await authenticate_user(UserRepository(db), form_data.username, form_data.password)
    return create_token_for_user(user_id=user.id)
