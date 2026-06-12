"""
RAG App — Streamlit UI
-----------------------
This file is the front-end. It lets the user:
1. Upload a PDF or TXT file
2. Ask questions about it
3. See the AI's answer
"""

import os
import tempfile
import streamlit as st
from rag import build_index, ask

st.set_page_config(page_title="📄 RAG App", page_icon="📄")

st.title("📄 Ask Your Document")
st.write("Upload a PDF or TXT file, then ask questions about it!")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["pdf", "txt"],
    help="Upload a PDF or plain text file",
)

if uploaded_file is not None:

    # Use file content instead of filename
    file_bytes = uploaded_file.getvalue()

    # Rebuild index only if file content changed
    if (
        "indexed_file" not in st.session_state
        or st.session_state.indexed_file != file_bytes
    ):

        with st.spinner("📚 Reading and indexing your document... (this takes a moment)"):

            suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".txt"

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            try:
                # Build fresh index for this uploaded file
                st.session_state.qa_chain = build_index(tmp_path)

                # Store actual file content signature
                st.session_state.indexed_file = file_bytes

            except Exception as e:
                st.error(f"❌ Failed to index document: {e}")
                st.stop()

            finally:
                os.unlink(tmp_path)

        st.success(f"✅ '{uploaded_file.name}' indexed successfully!")

    # Question input
    question = st.text_input(
        "💬 Ask a question about your document",
        placeholder="e.g. What is the main topic of this document?",
    )

    if question:
        with st.spinner("🤔 Thinking..."):
            answer = ask(st.session_state.qa_chain, question)

        st.write("### 📝 Answer")
        st.write(answer)