from pathlib import Path
import chromadb
import ollama

DATA_PATH = Path("data/employee_handbook.txt")
DB_PATH = "./chroma_db"
COLLECTION_NAME = "company_knowledge"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def load_documents():
    text = DATA_PATH.read_text(encoding="utf-8-sig")
    sections = [s.strip() for s in text.split("\n\n") if s.strip()]

    collection.upsert(
        ids=[f"section_{i}" for i in range(len(sections))],
        documents=sections,
        metadatas=[{"source": DATA_PATH.name} for _ in sections]
    )
    print(f"Indexed {len(sections)} document sections.")

def ask_question(question):
    results = collection.query(
        query_texts=[question],
        n_results=min(3, collection.count())
    )

    context = "\n\n".join(results["documents"][0])

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise knowledge assistant. "
                    "Answer only using the provided context. "
                    "If the answer is not in the context, say you don't know. "
                    "Do not invent company policies."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    print("\nANSWER:\n", response["message"]["content"])
    print("\nSOURCE:", DATA_PATH.name)

if __name__ == "__main__":
    load_documents()
    print("\nEnterprise AI Knowledge Assistant is ready!")
    while True:
        question = input("\nAsk a question (or type exit): ")
        if question.lower() == "exit":
            break
        ask_question(question)
