
import chromadb
import ollama

MODEL = "llama3.2:3b"


def initialise_database():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(name="company_knowledge")


def ask_question(question, collection):
    if collection.count() == 0:
        return {
            "answer": "I don't know. No documents have been indexed.",
            "sources": []
        }

    results = collection.query(
        query_texts=[question],
        n_results=min(1, collection.count()),
        include=["documents", "distances"]
    )

    documents = results["documents"][0]
    context = "\n\n".join(documents)

    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise knowledge assistant. "
                    "Answer only using the provided context. "
                    "Include all relevant entitlements, exceptions, and conditions "
                    "explicitly stated in the source. "
                    "For annual leave questions, distinguish paid annual leave "
                    "from additional public or bank holidays when mentioned. "
                    "If the answer is not available, say you don't know. "
                    "Never invent company policies. "
"Before answering, identify every condition, approval requirement, "
"limit, and exception in the context that applies to the question. "
"Include those relevant conditions in the final answer, "
"even if the question asks only for a number or quantity."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    draft_answer = response["message"]["content"]
    validation = ollama.chat(
        model=MODEL,
        options={"temperature": 0},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict factual answer editor. "
                    "Produce a complete factual answer to the user's question. "
"Use the source as the authority, not just the draft answer. "
"Preserve every relevant condition, approval requirement, "
"limit, and exception explicitly stated in the source. "
"Do not omit manager approvals or other requirements "
"when answering questions about quantities or entitlements. "
                    "Include all relevant facts explicitly supported by the source. "
                    "Do not add general knowledge, assumptions, or unsupported details. "
                    "Do not mention drafts, reviews, corrections, or your reasoning. "
                    "Output only the answer itself, without any introduction. "
                    "If the source does not contain the answer, say you don't know."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Source:\n{context}\n\n"
                    f"Draft answer:\n{draft_answer}"
                )
            }
        ]
    )
    return {
        "answer": validation["message"]["content"],
        "sources": documents
    }
