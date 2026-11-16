import hashlib

def hash_password(password: str) -> str:
    # Demo only: use a password hashing algorithm such as Argon2 or bcrypt in production.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
