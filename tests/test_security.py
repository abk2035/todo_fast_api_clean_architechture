from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.core.config import settings
from datetime import timedelta


def test_password_hash_and_verify():
    raw = "strong_pass_123"
    hashed = get_password_hash(raw)
    assert verify_password(raw, hashed)


def test_jwt_token_creation_and_decode():
    claims = {"user_id": 99}
    token = create_access_token(data=claims, expires_delta=timedelta(minutes=1))
    decoded = decode_access_token(token)
    assert decoded["user_id"] == claims["user_id"]
