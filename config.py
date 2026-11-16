from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

# Explicitly load from your parent directory .env file
ENV_PATH = Path(r"C:\Education\Code\AgenticAI\PRACTICE_SELF\.env")
load_dotenv(dotenv_path=ENV_PATH)

REPO_DIR = PROJECT_ROOT / "data" / "sample_repository"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

COLLECTION_NAME = "codebase_python"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

SUPPORTED_EXTENSIONS = {".py"}

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    "dist", "build", ".mypy_cache", ".pytest_cache", ".idea", ".vscode"
}
EXCLUDED_FILENAMES = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519"
}
MAX_FILE_BYTES = 1_000_000
CHUNK_MAX_CHARS = 1800
CHUNK_OVERLAP_LINES = 3
TOP_K = 5



# from pathlib import Path

# PROJECT_ROOT = Path(__file__).resolve().parent
# REPO_DIR = PROJECT_ROOT / "data" / "sample_repository"
# ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
# VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

# COLLECTION_NAME = "codebase_python"
# EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# SUPPORTED_EXTENSIONS = {".py"}

# EXCLUDED_DIRS = {
#     ".git", ".venv", "venv", "__pycache__", "node_modules",
#     "dist", "build", ".mypy_cache", ".pytest_cache", ".idea", ".vscode"
# }
# EXCLUDED_FILENAMES = {
#     ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519"
# }
# MAX_FILE_BYTES = 1_000_000
# CHUNK_MAX_CHARS = 1800
# CHUNK_OVERLAP_LINES = 3
# TOP_K = 5






# #----TO RUN----
# # ..\..\.venv\Scripts\Activate.ps1
# # streamlit run .\__pycache__\app.py
# # (inside __pycache__)
# # streamlit run app.py