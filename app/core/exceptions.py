from fastapi import HTTPException

class AppError(Exception):
    """Base exception d'application."""
    pass

class FunctionalError(AppError):
    """Erreur métier attendue, renvoyée à l'utilisateur."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class TechnicalError(AppError):
    """Erreur technique inattendue, interne."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


def handle_app_error(exception: AppError):
    """Translate AppError en HTTPException pour FastAPI."""
    if isinstance(exception, FunctionalError):
        raise HTTPException(status_code=exception.status_code, detail=exception.message)
    if isinstance(exception, TechnicalError):
        raise HTTPException(status_code=exception.status_code, detail=exception.message)
    raise HTTPException(status_code=500, detail="Erreur interne")
