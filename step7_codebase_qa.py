from step6_generate_answer import generate_answer

def main():
    print("Codebase RAG Q&A (type 'exit' to quit)")
    while True:
        question = input("\nAsk about your codebase: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue
        try:
            answer = generate_answer(question)
            print("\nAnswer:\n")
            print(answer)
        except Exception as exc:
            print(f"Error: {exc}")
            print("Check that steps 1-4 completed successfully.")

if __name__ == "__main__":
    main()
