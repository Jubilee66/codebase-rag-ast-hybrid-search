from data.sample_repository.config import PASSWORD_MIN_LENGTH
from data.sample_repository.database.db import find_user, save_user
from data.sample_repository.models.user import User
from data.sample_repository.utils.security import hash_password

def register_user(email: str, password: str) -> dict:
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError("Password is too short")
    if find_user(email):
        raise ValueError("User already exists")

    user = User(email=email, password_hash=hash_password(password))
    return save_user(user.to_dict())

def get_user(email: str):
    return find_user(email)
