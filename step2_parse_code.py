#-------------------------
# AST-based code parsing
#-------------------------
import json
from config import REPO_DIR, ARTIFACTS_DIR
from utils.code_parser import parse_python_file

def main():
    input_path = ARTIFACTS_DIR / "repository_files.json"
    if not input_path.exists():
        raise FileNotFoundError("Run step1_ingest_repository.py first.")

    records = json.loads(input_path.read_text(encoding="utf-8"))
    all_symbols = []

    for record in records:
        path = REPO_DIR / record["file_path"]
        symbols = parse_python_file(path, REPO_DIR, record["content"])
        all_symbols.extend(symbols)
        print(f'{record["file_path"]}: {len(symbols)} symbols')

    output = ARTIFACTS_DIR / "parsed_symbols.json"
    output.write_text(json.dumps(all_symbols, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nTotal symbols: {len(all_symbols)}")
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
