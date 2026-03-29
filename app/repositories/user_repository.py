from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User
from app.schemas.user import UserCreate


class UserRepository:
    """Repository pour opérations sur les utilisateurs en base."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Récupère un utilisateur via son adresse email."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def create(self, user_create: UserCreate, hashed_password: str) -> User:
        user = User(email=user_create.email, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
