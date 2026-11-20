
import streamlit as st
from assistant import initialise_database, ask_question

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
def load_database():
    return initialise_database()


collection = load_database()

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
            result = ask_question(question, collection)
            answer = result["answer"]
            documents = result["sources"]

            st.markdown(answer)

            with st.expander("📄 View Sources"):
                for i, document in enumerate(documents, 1):
                    st.markdown(f"**Retrieved Section {i}**")
                    st.write(document)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
