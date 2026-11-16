import ast
from pathlib import Path

def _node_source(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node)
    return segment if segment else ""

def parse_python_file(path: Path, repo_root: Path, source: str) -> list[dict]:
    relative_path = str(path.relative_to(repo_root)).replace("\\", "/")
    try:
        tree = ast.parse(source, filename=relative_path)
    except SyntaxError as exc:
        return [{
            "symbol_type": "parse_error",
            "symbol_name": relative_path,
            "file_path": relative_path,
            "start_line": getattr(exc, "lineno", 1) or 1,
            "end_line": getattr(exc, "end_lineno", None) or getattr(exc, "lineno", 1) or 1,
            "code": source,
            "docstring": "",
            "imports": [],
        }]

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append(module)

    symbols = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Avoid treating nested methods/functions as independent top-level chunks here.
            # They are still discovered by ast.walk and receive their own chunks.
            symbols.append({
                "symbol_type": "class" if isinstance(node, ast.ClassDef) else "function",
                "symbol_name": node.name,
                "file_path": relative_path,
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "code": _node_source(source, node),
                "docstring": ast.get_docstring(node) or "",
                "imports": sorted(set(imports)),
            })

    if not symbols:
        symbols.append({
            "symbol_type": "module",
            "symbol_name": Path(relative_path).name,
            "file_path": relative_path,
            "start_line": 1,
            "end_line": max(1, len(source.splitlines())),
            "code": source,
            "docstring": ast.get_docstring(tree) or "",
            "imports": sorted(set(imports)),
        })

    return symbols
