import json
from config import ARTIFACTS_DIR, VECTOR_DB_DIR, COLLECTION_NAME
from utils.embedding_utils import get_embedding_model
import chromadb

def main():
    chunks_path = ARTIFACTS_DIR / "code_chunks.json"
    if not chunks_path.exists():
        raise FileNotFoundError("Run step3_chunk_code.py first.")

    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    
    if not chunks:
        print("No chunks found to store.")
        return

    print(f"Loading embedding model...")
    model = get_embedding_model()

    # Prepare data for ChromaDB
    texts = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        # Support both old and new keys for safety
        source = chunk.get("source") or chunk.get("file_path", "unknown")
        chunk_type = chunk.get("type") or chunk.get("symbol_type", "block")
        name = chunk.get("name") or chunk.get("symbol_name", "unknown")
        content = chunk.get("content", "")

        # Rich text layout for embedding representation
        rich_text = f"File: {source}\nType: {chunk_type} {name}\nLines {chunk.get('start_line', 0)}-{chunk.get('end_line', 0)}\n\n{content}"
        texts.append(rich_text)

        metadatas.append({
            "source": str(source),
            "type": str(chunk_type),
            "name": str(name),
            "start_line": int(chunk.get("start_line", 0)),
            "end_line": int(chunk.get("end_line", 0))
        })
        ids.append(f"chunk_{i}")

    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    print(f"Storing into ChromaDB at {VECTOR_DB_DIR}...")
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # Upsert chunks into ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Vector store ready. Collection: {COLLECTION_NAME}, chunks: {collection.count()}")

if __name__ == "__main__":
    main()