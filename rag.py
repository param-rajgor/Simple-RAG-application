"""
RAG (Retrieval-Augmented Generation) Logic
"""

import os
import shutil
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

from langchain_community.embeddings import HuggingFaceEmbeddings


from langchain.chains import RetrievalQA

load_dotenv()

CHROMA_DIR = "./chroma_db"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def build_index(file_path: str):

    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    # Load document
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    # Split document
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    # Gemini Embeddings
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return qa_chain


def ask(qa_chain, question: str) -> str:
    result = qa_chain.invoke(
        {"query": question}
    )
    return result["result"]