from passlib.handlers.pbkdf2 import pbkdf2_sha256


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password_text: str, password_hash: str) -> bool:
    return pbkdf2_sha256.verify(password_text, password_hash)
