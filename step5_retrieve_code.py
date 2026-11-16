
import argparse
import chromadb
from config import VECTOR_DB_DIR, COLLECTION_NAME, TOP_K
from utils.embedding_utils import embed_texts

def retrieve(query: str, top_k: int = TOP_K):
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    collection = client.get_collection(COLLECTION_NAME)
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for document, metadata, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({"content": document, "metadata": metadata, "distance": distance})
    return hits

def main():
    parser = argparse.ArgumentParser(description="Retrieve code snippets from the codebase RAG vector store.")
    parser.add_argument("query", help='Question about the repository (e.g., "save_user"|"authenticate user"|"database connection")')
    parser.add_argument("--top-k", type=int, default=TOP_K, help="Number of top results to retrieve")
    args = parser.parse_args()

    hits = retrieve(args.query, args.top_k)
    for rank, hit in enumerate(hits, 1):
        m = hit["metadata"]
        # Safe extraction with fallbacks
        source = m.get("source") or m.get("file_path") or "unknown"
        symbol_type = m.get("type") or m.get("symbol_type") or "block"
        symbol_name = m.get("name") or m.get("symbol_name") or "unknown"
        start_line = m.get("start_line", 1)
        end_line = m.get("end_line", 1)

        print("\n" + "=" * 75)
        print(f"#{rank} {source} | {symbol_type} {symbol_name}")
        print(f"Lines: {start_line}-{end_line} | Distance: {hit['distance']:.4f}")
        print(hit["content"])

if __name__ == "__main__":
    main()
#===============================================
# TO RUN:
# python step5_retrieve_code.py "what is database use here"    
#================================================

# import argparse
# import chromadb
# from config import VECTOR_DB_DIR, COLLECTION_NAME, TOP_K
# from utils.embedding_utils import embed_texts
# # from RAG.codebase_rag_project.config import VECTOR_DB_DIR, COLLECTION_NAME, TOP_K
# # from RAG.codebase_rag_project.utils.embedding_utils import embed_texts

# def retrieve(query: str, top_k: int = TOP_K):
#     client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
#     collection = client.get_collection(COLLECTION_NAME)
#     query_embedding = embed_texts([query])[0]

#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=min(top_k, collection.count()),
#         include=["documents", "metadatas", "distances"],
#     )

#     hits = []
#     for document, metadata, distance in zip(
#         results["documents"][0], results["metadatas"][0], results["distances"][0]
#     ):
#         hits.append({"content": document, "metadata": metadata, "distance": distance})
#     return hits

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("query", help="Question about the repository")
#     parser.add_argument("--top-k", type=int, default=TOP_K)
#     args = parser.parse_args()

#     hits = retrieve(args.query, args.top_k)
#     for rank, hit in enumerate(hits, 1):
#         m = hit["metadata"]
#         print("\n" + "=" * 75)
#         print(f'#{rank} {m["file_path"]} | {m["symbol_type"]} {m["symbol_name"]}')
#         print(f'Lines: {m["start_line"]}-{m["end_line"]} | Distance: {hit["distance"]:.4f}')
#         print(hit["content"])

# if __name__ == "__main__":
#     main()
#     # step5_retrieve_code.py: error: the following arguments are required: query(eg:"save_user"|"authenticate user"|"database connection")
# # python step5_retrieve_code.py "save_user"