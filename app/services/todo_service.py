from app.core.exceptions import FunctionalError
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate


async def create_todo(repo: TodoRepository, owner_id: int, todo_data: TodoCreate):
    """Créer une nouvelle todo pour le propriétaire donné."""
    return await repo.create(owner_id=owner_id, todo_create=todo_data)


async def get_todos(repo: TodoRepository, owner_id: int):
    """Liste toutes les todos d'un utilisateur (owner_id)."""
    return await repo.get_all_by_owner(owner_id)


async def get_todo(repo: TodoRepository, owner_id: int, todo_id: int):
    todo = await repo.get_by_id(todo_id=todo_id, owner_id=owner_id)
    if not todo:
        raise FunctionalError("Todo introuvable", status_code=404)
    return todo


async def update_todo(repo: TodoRepository, owner_id: int, todo_id: int, todo_data: TodoUpdate):
    todo = await get_todo(repo, owner_id, todo_id)
    return await repo.update(todo, todo_data)


async def remove_todo(repo: TodoRepository, owner_id: int, todo_id: int):
    todo = await get_todo(repo, owner_id, todo_id)
    await repo.delete(todo)
    return True
