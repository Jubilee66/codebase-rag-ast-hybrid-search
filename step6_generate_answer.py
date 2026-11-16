#====================AFTER ATS CHUNKING===========================
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from step5_retrieve_code import retrieve
from config import ENV_PATH

SYSTEM_PROMPT = (
    "You are a senior software engineer helping explain a code repository. "
    "Answer only from the supplied code context. If the context is insufficient, "
    "say what is missing instead of inventing behavior. Cite file paths and line "
    "ranges from the metadata. Distinguish facts from reasonable inferences."
)

def generate_answer(question: str, top_k: int = 5) -> str:
    hits = retrieve(question, top_k)
    if not hits:
        return "No relevant code was retrieved."

    context_parts = []
    for hit in hits:
        m = hit["metadata"]
        context_parts.append(
            f'FILE: {m.get("file_path", m.get("source", "unknown"))}\n'
            f'SYMBOL: {m.get("symbol_type", m.get("type", ""))} {m.get("symbol_name", m.get("name", ""))}\n'
            f'LINES: {m.get("start_line", 1)}-{m.get("end_line", 1)}\n'
            f'{hit["content"]}'
        )
    context = "\n\n---\n\n".join(context_parts)

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return f"GROQ_API_KEY is missing from environment variables. Checked path: {ENV_PATH}"

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=api_key,
    )
    
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Question: {question}\n\nRetrieved code context:\n{context}")
    ])
    return response.content

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "How do I connect to the database?"
    print(generate_answer(query))
#====================BEFORE ATS CHUNKING===========================
# import argparse
# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.messages import HumanMessage, SystemMessage
# from step5_retrieve_code import retrieve

# SYSTEM_PROMPT = (
#     "You are a senior software engineer helping explain a code repository. "
#     "Answer only from the supplied code context. If the context is insufficient, "
#     "say what is missing instead of inventing behavior. Cite file paths and line "
#     "ranges from the metadata. Distinguish facts from reasonable inferences."
# )

# def generate_answer(question: str, top_k: int = 5) -> str:
#     hits = retrieve(question, top_k)
#     if not hits:
#         return "No relevant code was retrieved."

#     context_parts = []
#     for hit in hits:
#         m = hit["metadata"]
#         context_parts.append(
#             f'FILE: {m["file_path"]}\n'
#             f'SYMBOL: {m["symbol_type"]} {m["symbol_name"]}\n'
#             f'LINES: {m["start_line"]}-{m["end_line"]}\n'
#             f'{hit["content"]}'
#         )
#     context = "\n\n---\n\n".join(context_parts)

#     load_dotenv()
#     api_key = os.getenv("GROQ_API_KEY")
#     if not api_key:
#         return (
#             "GROQ_API_KEY is not configured. Retrieved context is shown below; "
#             "add your key to .env to enable generated answers.\n\n" + context
#         )

#     llm = ChatGroq(
#         model="openai/gpt-oss-120b",   #"llama-3.3-70b-versatile"
#         temperature=0,
#         api_key=api_key,
#     )
#     response = llm.invoke([
#         SystemMessage(content=SYSTEM_PROMPT),
#         HumanMessage(content=f"Question: {question}\n\nRetrieved code context:\n{context}")
#     ])
#     return response.content

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("query", help="Question about the repository")
#     parser.add_argument("--top-k", type=int, default=5)
#     args = parser.parse_args()
#     print(generate_answer(args.query, args.top_k))

# if __name__ == "__main__":
#     main()


# step6_generate_answer.py: error: the following arguments are required: query'(eg :"Trace the entire execution flow of registering a new user from main.py down to database/db.py."
# "How does the authentication function verify a user, and which files are involved in the process?")
# "Where is password hashing handled, and what algorithm or utility does it use?"
# "Are there any password length or complexity constraints enforced in the codebase, and where are they checked?"
# "What is the difference between how config.py defines the database and how database/db.py actually stores data?"
# "Which functions modify the user store, and how are updates handled?"
# "Which service files import security utilities, and what functions do they call?"
# "What does the run_demo function in main.py test, and what helper functions does it rely on?"

# python step6_generate_answer.py "How do I connect to the database?"