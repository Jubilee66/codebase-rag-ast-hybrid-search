#===============AST-Based Chunking=================================================
# AFTER UPDATING RE RUN 
# python step1_ingest_repository.py
# python step2_parse_code.py
# python step3_chunk_code.py
# python step4_build_vector_store.py

#---test---
# python step7_codebase_qa.py
#================================================================================
import ast
from typing import List, Dict, Any

class ASTCodeChunker:
    """
    Splits Python source code into logical chunks based on AST nodes (Classes, Functions, 
    and Module-level blocks) with robust line range handling and fallbacks.
    """
    def __init__(self, max_chunk_chars: int = 1800):
        self.max_chunk_chars = max_chunk_chars

    def chunk_file(self, file_path: str, code_content: str) -> List[Dict[str, Any]]:
        lines = code_content.splitlines()
        total_lines = len(lines)
        
        if total_lines == 0:
            return self._fallback_chunk(file_path, code_content, 1)

        try:
            tree = ast.parse(code_content)
        except SyntaxError:
            return self._fallback_chunk(file_path, code_content, total_lines)

        chunks = []
        covered_lines = set()

        # 1. Extract classes, functions, and async functions
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                start_line = getattr(node, 'lineno', 1)
                end_line = getattr(node, 'end_lineno', start_line)
                
                # Ensure valid slice boundaries
                start_idx = max(0, start_line - 1)
                end_idx = min(total_lines, end_line)
                
                node_lines = lines[start_idx:end_idx]
                chunk_text = "\n".join(node_lines)
                
                for l in range(start_line, end_line + 1):
                    covered_lines.add(l)

                chunks.append({
                    "source": file_path,
                    "type": node.__class__.__name__.lower(),
                    "name": getattr(node, 'name', 'unknown'),
                    "content": chunk_text,
                    "start_line": start_line,
                    "end_line": max(start_line, end_line)
                })

        # 2. Capture remaining uncovered lines (module-level blocks, imports, variables)
        current_block = []
        block_start = 1

        for idx, line in enumerate(lines, start=1):
            if idx not in covered_lines:
                if not current_block:
                    block_start = idx
                current_block.append(line)
            else:
                if current_block:
                    text = "\n".join(current_block)
                    if text.strip():
                        b_end = block_start + len(current_block) - 1
                        chunks.append({
                            "source": file_path,
                            "type": "module_block",
                            "name": "global_scope",
                            "content": text,
                            "start_line": block_start,
                            "end_line": max(block_start, b_end)
                        })
                    current_block = []

        if current_block:
            text = "\n".join(current_block)
            if text.strip():
                b_end = block_start + len(current_block) - 1
                chunks.append({
                    "source": file_path,
                    "type": "module_block",
                    "name": "global_scope",
                    "content": text,
                    "start_line": block_start,
                    "end_line": max(block_start, b_end)
                })

        if not chunks:
            return self._fallback_chunk(file_path, code_content, total_lines)

        return chunks

    def _fallback_chunk(self, file_path: str, code_content: str, total_lines: int) -> List[Dict[str, Any]]:
        return [{
            "source": file_path,
            "type": "fallback",
            "name": "full_file",
            "content": code_content,
            "start_line": 1,
            "end_line": max(1, total_lines)
        }]
#============================


#===========================================================================================
# # ==========splits text based on character counts or line counts with an overlap,
# #  While simple and effective, this approach is syntactically blind. It might slice right through the middle of a complex function, cutting a def calculate_total()
# from RAG.codebase_rag_project.config import CHUNK_MAX_CHARS, CHUNK_OVERLAP_LINES

# def _split_large_code(code: str, max_chars: int, overlap_lines: int) -> list[tuple[int, int, str]]:
#     lines = code.splitlines()
#     if not lines:
#         return [(1, 1, code)] if code else []

#     chunks = []
#     start = 0
#     while start < len(lines):
#         end = start
#         char_count = 0
#         while end < len(lines):
#             next_len = len(lines[end]) + 1
#             if end > start and char_count + next_len > max_chars:
#                 break
#             char_count += next_len
#             end += 1

#         body = "\n".join(lines[start:end])
#         chunks.append((start + 1, end, body))
#         if end >= len(lines):
#             break
#         start = max(start + 1, end - overlap_lines)

#     return chunks

# def make_code_chunks(symbols: list[dict]) -> list[dict]:
#     chunks = []
#     for symbol in symbols:
#         code = symbol.get("code", "")
#         if not code.strip():
#             continue

#         pieces = _split_large_code(code, CHUNK_MAX_CHARS, CHUNK_OVERLAP_LINES)
#         for part_index, (relative_start, relative_end, piece) in enumerate(pieces):
#             absolute_start = symbol["start_line"] + relative_start - 1
#             absolute_end = min(symbol["end_line"], symbol["start_line"] + relative_end - 1)
#             chunks.append({
#                 "chunk_id": f'{symbol["file_path"]}:{symbol["symbol_name"]}:{part_index}',
#                 "file_path": symbol["file_path"],
#                 "symbol_name": symbol["symbol_name"],
#                 "symbol_type": symbol["symbol_type"],
#                 "start_line": absolute_start,
#                 "end_line": absolute_end,
#                 "docstring": symbol.get("docstring", ""),
#                 "imports": symbol.get("imports", []),
#                 "content": piece,
#             })
#     return chunks
