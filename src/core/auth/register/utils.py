import bcrypt
import secrets


def hashed_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_hash_password(hashed_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


async def check_confirm_password_with_password(
    password: str, confirm_password: str
) -> bool:
    if password != confirm_password:
        return False
    return True
