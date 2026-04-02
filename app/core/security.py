from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
import bcrypt

from app.core.config import settings
import hashlib


def preprocess_password(password: str) -> str:
    """Pré-traite le mot de passe utilisateur avant hashing (sha256 hex)."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie que le mot de passe fourni correspond au hash stocké."""
    processed = preprocess_password(plain_password).encode()
    return bcrypt.checkpw(processed, hashed_password.encode())


def get_password_hash(password: str) -> str:
    """Hash un mot de passe en sha256 puis bcrypt."""
    processed = preprocess_password(password).encode()
    hashed = bcrypt.hashpw(processed, bcrypt.gensalt())
    return hashed.decode()


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Crée un JWT signé avec expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """Décode un JWT et renvoie le contenu payload."""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload
