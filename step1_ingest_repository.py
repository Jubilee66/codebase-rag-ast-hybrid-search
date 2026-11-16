import json
from config import REPO_DIR, ARTIFACTS_DIR
from utils.repo_loader import discover_python_files, read_source_file

def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    paths = discover_python_files(REPO_DIR)

    records = []
    for path in paths:
        try:
            content = read_source_file(path)
            records.append({
                "file_path": str(path.relative_to(REPO_DIR)).replace("\\", "/"),
                "content": content,
                "size_bytes": path.stat().st_size,
            })
            print(f"Ingested: {path.name} ({len(content)} characters)")
        except Exception as exc:
            print(f"Could not read {path}: {exc}")

    output = ARTIFACTS_DIR / "repository_files.json"
    output.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nFiles discovered: {len(paths)}")
    print(f"Files ingested: {len(records)}")
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
