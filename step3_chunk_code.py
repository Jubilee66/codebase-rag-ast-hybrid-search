#=========================After ASTCode chunker====================================================
import json
from typing import List, Dict, Any
from config import ARTIFACTS_DIR
from utils.code_chunker import ASTCodeChunker

def main():
    # Read raw repository files directly instead of pre-parsed symbols
    input_path = ARTIFACTS_DIR / "repository_files.json"
    if not input_path.exists():
        raise FileNotFoundError("Run step1_ingest_repository.py first.")

    files_data = json.loads(input_path.read_text(encoding="utf-8"))
    chunker = ASTCodeChunker()
    
    chunks = []
    # repository_files.json typically stores files as a dict {path: content} or list of objects
    if isinstance(files_data, dict):
        file_items = files_data.items()
    else:
        file_items = [(f.get("file_path") or f.get("source"), f.get("content", "")) for f in files_data]

    for file_path, content in file_items:
        if not content.strip():
            continue
        file_chunks = chunker.chunk_file(file_path, content)
        chunks.extend(file_chunks)

    output = ARTIFACTS_DIR / "code_chunks.json"
    output.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Files processed: {len(file_items)}")
    print(f"Code chunks created: {len(chunks)}")
    for chunk in chunks[:3]:
        print("\n" + "=" * 60)
        print(f"{chunk['source']} | {chunk['type']} | {chunk['name']}")
        print(f"Lines {chunk['start_line']}-{chunk['end_line']}")
        print(chunk["content"][:400])
    print(f"\nSaved: {output}")

if __name__ == "__main__":
    main()
#========================Before ATSCodeChunker=====================================================
# import json
# from config import ARTIFACTS_DIR
# from RAG_3_CodeBaseRAG.utils.code_chunker import make_code_chunks

# def main():
#     input_path = ARTIFACTS_DIR / "parsed_symbols.json"
#     if not input_path.exists():
#         raise FileNotFoundError("Run step2_parse_code.py first.")

#     symbols = json.loads(input_path.read_text(encoding="utf-8"))
#     chunks = make_code_chunks(symbols)

#     output = ARTIFACTS_DIR / "code_chunks.json"
#     output.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")

#     print(f"Symbols received: {len(symbols)}")
#     print(f"Code chunks created: {len(chunks)}")
#     for chunk in chunks[:3]:
#         print("\n" + "=" * 60)
#         print(f'{chunk["file_path"]} | {chunk["symbol_type"]} | {chunk["symbol_name"]}')
#         print(f'Lines {chunk["start_line"]}-{chunk["end_line"]}')
#         print(chunk["content"][:400])
#     print(f"\nSaved: {output}")

# if __name__ == "__main__":
#     main()
