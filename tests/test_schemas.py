from app.schemas.user import UserCreate
from app.schemas.todo import TodoCreate, TodoUpdate


def test_user_create_validation():
    u = UserCreate(email="utilisateur@example.com", password="motdepasse123")
    assert u.email == "utilisateur@example.com"


def test_todo_schema_validation():
    todo = TodoCreate(title="Acheter du lait")
    assert todo.title == "Acheter du lait"
    update = TodoUpdate(title="Acheter du pain", completed=True)
    assert update.title == "Acheter du pain"
    assert update.completed is True
