import streamlit as st
import ollama
import chromadb
from pathlib import Path

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise AI Knowledge Assistant")
st.caption("Powered by Llama 3.2 | Ollama | ChromaDB | RAG")

with st.sidebar:
    st.header("System Information")
    st.success("Local AI System")
    st.write("**Model:** Llama 3.2 (3B)")
    st.write("**Inference Engine:** Ollama")
    st.write("**Vector Database:** ChromaDB")
    st.write("**Architecture:** RAG")
    st.divider()
    st.info("Enterprise AI Portfolio Project")

@st.cache_resource
def initialise_database():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="company_knowledge"
    )
    return collection

collection = initialise_database()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about company policies...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching company knowledge..."):

            results = collection.query(
                query_texts=[question],
                n_results=min(3, collection.count())
            )

            documents = results["documents"][0]
            context = "\n\n".join(documents)

            response = ollama.chat(
                model="llama3.2:3b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an enterprise knowledge assistant. "
                            "Answer only using the provided context. "
                            "If the answer is not available, say you don't know. "
                            "Never invent company policies."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{context}\n\n"
                            f"Question: {question}"
                        )
                    }
                ]
            )

            answer = response["message"]["content"]
            st.markdown(answer)

            with st.expander("📄 View Sources"):
                for i, document in enumerate(documents, 1):
                    st.markdown(f"**Retrieved Section {i}**")
                    st.write(document)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })