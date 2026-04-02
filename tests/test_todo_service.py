import pytest
from app.services.todo_service import get_todo, get_todos, create_todo, update_todo, remove_todo
from app.core.exceptions import FunctionalError
from app.schemas.todo import TodoCreate, TodoUpdate


class FakeTodo:
    def __init__(self, id, owner_id, title, description=None, completed=False):
        self.id = id
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.completed = completed


class FakeRepo:
    def __init__(self):
        self.todos = {
            1: FakeTodo(1, 1, "Test", "desc"),
        }

    async def get_all_by_owner(self, owner_id):
        return [t for t in self.todos.values() if t.owner_id == owner_id]

    async def get_by_id(self, todo_id, owner_id):
        todo = self.todos.get(todo_id)
        return todo if todo and todo.owner_id == owner_id else None

    async def create(self, owner_id, todo_create):
        new_id = max(self.todos.keys()) + 1
        todo = FakeTodo(new_id, owner_id, todo_create.title, todo_create.description or "")
        self.todos[new_id] = todo
        return todo

    async def update(self, todo, todo_update):
        if todo_update.title is not None:
            todo.title = todo_update.title
        if todo_update.description is not None:
            todo.description = todo_update.description
        if todo_update.completed is not None:
            todo.completed = todo_update.completed
        return todo

    async def delete(self, todo):
        del self.todos[todo.id]


@pytest.mark.anyio
async def test_todo_lifecycle():
    repo = FakeRepo()
    todos = await get_todos(repo, 1)
    assert len(todos) == 1

    new = await create_todo(repo, 1, TodoCreate(title="Nouvelle tâche"))
    assert new.title == "Nouvelle tâche"

    got = await get_todo(repo, 1, new.id)
    assert got.id == new.id

    updated = await update_todo(repo, 1, new.id, TodoUpdate(completed=True))
    assert updated.completed is True

    await remove_todo(repo, 1, new.id)
    with pytest.raises(FunctionalError):
        await get_todo(repo, 1, new.id)
