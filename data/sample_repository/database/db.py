_USERS = {}

def save_user(user: dict) -> dict:
    _USERS[user["email"]] = user
    return user

def find_user(email: str):
    return _USERS.get(email)

def list_users() -> list[dict]:
    return list(_USERS.values())
