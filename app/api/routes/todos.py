from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoRead, TodoUpdate
from app.services.todo_service import create_todo, get_todos, get_todo, update_todo, remove_todo

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.post("/", response_model=TodoRead)
async def create_new_todo(
    incoming: TodoCreate,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Création d'une todo pour l'utilisateur authentifié."""
    return await create_todo(TodoRepository(db), current_user.id, incoming)


@router.get("/", response_model=list[TodoRead])
async def list_todos(current_user=Depends(get_current_user), db=Depends(get_db)):
    """Retourne la liste des todos de l'utilisateur courant."""
    return await get_todos(TodoRepository(db), current_user.id)


@router.get("/{todo_id}", response_model=TodoRead)
async def read_todo(todo_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    return await get_todo(TodoRepository(db), current_user.id, todo_id)


@router.put("/{todo_id}", response_model=TodoRead)
async def modify_todo(
    todo_id: int,
    incoming: TodoUpdate,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return await update_todo(TodoRepository(db), current_user.id, todo_id, incoming)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    await remove_todo(TodoRepository(db), current_user.id, todo_id)
    return {"message": "Todo supprimé avec succès"}
