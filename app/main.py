from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import auth, todos, users
from app.core.exceptions import AppError, FunctionalError, TechnicalError
from app.db import Base, models
from app.db.session import engine

# Instance FastAPI de l'application
app = FastAPI(title="Todo App Clean Architecture", version="1.0")


@app.on_event("startup")
async def on_startup():
    # Au démarrage, on synchronise le modèle SQLAlchemy avec la base.
    # En production, privilégier alembic pour les migrations de schéma.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    if isinstance(exc, FunctionalError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
    if isinstance(exc, TechnicalError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
    return JSONResponse(status_code=500, content={"detail": "Erreur interne"})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Gestion globale des exceptions non prévues
    return JSONResponse(status_code=500, content={"detail": "Erreur serveur inattendue"})

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)
