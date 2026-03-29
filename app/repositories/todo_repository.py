from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    """Repository pour la gestion des todos en base."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_by_owner(self, owner_id: int):
        result = await self.session.execute(select(Todo).where(Todo.owner_id == owner_id))
        return result.scalars().all()

    async def get_by_id(self, todo_id: int, owner_id: int):
        result = await self.session.execute(select(Todo).where(Todo.id == todo_id, Todo.owner_id == owner_id))
        return result.scalars().first()

    async def create(self, owner_id: int, todo_create: TodoCreate):
        todo = Todo(owner_id=owner_id, **todo_create.dict())
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def update(self, todo: Todo, todo_update: TodoUpdate):
        for field, value in todo_update.dict(exclude_unset=True).items():
            setattr(todo, field, value)
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def delete(self, todo: Todo):
        await self.session.delete(todo)
        await self.session.commit()
