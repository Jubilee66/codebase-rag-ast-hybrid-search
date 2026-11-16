# Codebase RAG (Python-first starter)

A small, modular Codebase RAG project. It ingests Python source files, extracts
syntax-aware chunks with Python AST, embeds them, stores them in ChromaDB, retrieves
relevant code, and optionally generates an answer with Groq.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env`. Add `GROQ_API_KEY` if you want LLM-generated answers.
The retrieval stage works without an API key.

## Run in order

Run commands from the project root:

```bash
python step1_ingest_repository.py
python step2_parse_code.py
python step3_chunk_code.py
python step4_build_vector_store.py
python step5_retrieve_code.py "Where is user authentication handled?"
python step6_generate_answer.py "Explain the user registration flow."
python step7_codebase_qa.py
```

The included repository is in `data/sample_repository/`. Replace it with another
Python repository later, or change `REPO_DIR` in `config.py`.

## Pipeline artifacts

- `artifacts/repository_files.json`: discovered source files
- `artifacts/parsed_symbols.json`: AST-extracted functions/classes and metadata
- `artifacts/code_chunks.json`: chunks ready for embedding
- `vector_db/`: persistent ChromaDB collection

## Important scope

This first version parses Python using the standard-library `ast` module. It is
not yet a multi-language parser. For JavaScript, Java, C#, etc., add Tree-sitter
in a later iteration. The default embedding model is a general-purpose baseline
(`all-MiniLM-L6-v2`), not a code-specialized embedding model. We can benchmark
code-specific models after the first end-to-end run.

The ingestion script skips common generated/vendor folders and likely secret files.
Review exclusions before indexing a production repository.
