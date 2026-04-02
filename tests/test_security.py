from app.core.security import get_password_hash, verify_password, preprocess_password, create_access_token, decode_access_token
from datetime import timedelta


def test_preprocess_password_sha256():
    raw = "strong_pass_123456"
    processed = preprocess_password(raw)
    assert processed != raw
    assert len(processed) == 64


def test_password_hash_and_verify_success():
    raw = "strong_pass_123456"
    hashed = get_password_hash(raw)

    assert hashed != raw
    assert verify_password(raw, hashed)


def test_password_verify_fail_for_wrong_password():
    raw = "strong_pass_123456"
    wrong = "weak_pass"
    hashed = get_password_hash(raw)

    assert not verify_password(wrong, hashed)


def test_jwt_token_creation_and_decode():
    claims = {"user_id": 99}
    token = create_access_token(data=claims, expires_delta=timedelta(minutes=1))
    decoded = decode_access_token(token)
    assert decoded["user_id"] == claims["user_id"]
