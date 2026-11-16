from pathlib import Path
from config import SUPPORTED_EXTENSIONS, EXCLUDED_DIRS, EXCLUDED_FILENAMES, MAX_FILE_BYTES

def discover_python_files(repo_dir: Path) -> list[Path]:
    if not repo_dir.exists():
        raise FileNotFoundError(f"Repository folder does not exist: {repo_dir}")

    discovered = []
    for path in repo_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.name in EXCLUDED_FILENAMES or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                print(f"Skipping large file: {path}")
                continue
        except OSError:
            continue
        discovered.append(path)

    return sorted(discovered)

def read_source_file(path: Path) -> str:
    # Python source is usually UTF-8; replacement avoids one bad byte stopping ingestion.
    return path.read_text(encoding="utf-8", errors="replace")
