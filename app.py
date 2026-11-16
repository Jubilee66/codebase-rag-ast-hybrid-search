#=======after updating utils\code_chunker.py(added ATS code chunker)=====================
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
from config import VECTOR_DB_DIR, COLLECTION_NAME

st.set_page_config(
    page_title="Codebase RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Codebase RAG Assistant")
st.markdown("Ask multiple questions about your repository in a continuous chat session.")

@st.cache_resource
def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Dynamically resolve path and collection name from central config
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)
    return model, collection

model, collection = load_resources()

# Initialize chat history in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "chunks" in message:
            with st.expander("View Retrieved Code Chunks"):
                for i, chunk_info in enumerate(message["chunks"], start=1):
                    st.markdown(f"**Source:** `{chunk_info['source']}`")
                    st.code(chunk_info["content"], language="python")

# Chat input widget that stays available
if query := st.chat_input("Ask a question about your codebase..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching codebase and generating answer..."):
            try:
                query_embedding = model.encode(query).tolist()
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=4
                )
                
                docs = results["documents"][0]
                metadatas = results["metadatas"][0]
                
                context = ""
                chunk_payloads = []
                for i, doc in enumerate(docs):
                    meta = metadatas[i] if i < len(metadatas) else {}
                    source = meta.get("source") or meta.get("file") or "unknown"
                    context += f"FILE: {source}\n---BEGIN CHUNK---\n{doc}\n---END CHUNK---\n\n"
                    chunk_payloads.append({"source": source, "content": doc})
                    
                prompt = f"""You are a professional Codebase RAG Assistant.
Answer the user question accurately using ONLY the provided code context. Include file names and relevant details where appropriate.

CODE CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

                response = ollama.chat(
                    model="llama3.2",
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = response["message"]["content"]
                
                st.markdown(answer)
                
                with st.expander("View Retrieved Code Chunks"):
                    for i, chunk_info in enumerate(chunk_payloads, start=1):
                        st.markdown(f"**Source:** `{chunk_info['source']}`")
                        st.code(chunk_info["content"], language="python")
                
                # Save assistant response to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "chunks": chunk_payloads
                })
                
            except Exception as e:
                error_msg = f"Error communicating with Ollama LLM: {e}"
                st.error(error_msg)
                st.info("Make sure Ollama is running locally with 'llama3.2' installed (`ollama run llama3.2`).")
#=====================================================================
# How do I connect to the database?

# Where is password hashing handled?

# Which service files import security utilities?
#==========================================================