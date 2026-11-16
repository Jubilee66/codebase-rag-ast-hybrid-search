from RAG.codebase_rag_project.data.sample_repository.database.db import find_user
from RAG.codebase_rag_project.data.sample_repository.utils.security import hash_password

def authenticate(email: str, password: str) -> bool:
    user = find_user(email)
    if user is None:
        return False
    return user["password_hash"] == hash_password(password)
