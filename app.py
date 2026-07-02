import streamlit as st
import os
from utils.ingestor import ingest_pdfs, load_vectorstore
from utils.retriever import answer_question

st.set_page_config(
    page_title="Valtruis Due Diligence Assistant",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Due Diligence RAG Assistant")
st.caption("Ask questions across uploaded healthcare company documents instantly.")

# Sidebar for uploads
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDFs (pitch decks, 10-Ks, reports)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Ingest Documents", type="primary"):
            with st.spinner("Processing documents..."):
                result = ingest_pdfs(uploaded_files)
                st.success(f"Ingested {result['chunks']} chunks from {result['docs']} documents.")
                st.session_state["ingested"] = True

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. Upload company PDFs")
    st.markdown("2. System chunks and indexes them")
    st.markdown("3. Ask any question in plain English")
    st.markdown("4. Get cited answers instantly")

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Example questions
if not st.session_state.messages:
    st.info("**Example questions you can ask:**\n"
            "- What is this company's revenue model?\n"
            "- What are the key risks mentioned?\n"
            "- How does this company define value-based care?\n"
            "- Who are the main competitors mentioned?\n"
            "- What are the growth projections?")

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            try:
                response = answer_question(prompt)
                st.markdown(response["answer"])
                if response.get("sources"):
                    with st.expander("Sources"):
                        for src in response["sources"]:
                            st.markdown(f"- {src}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"]
                })
            except Exception as e:
                err = f"Error: {str(e)}. Make sure you've uploaded and ingested documents first."
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
