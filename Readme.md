# 📄 Project 01 — Simple RAG Application

> **RAG** = Retrieval-Augmented Generation — a technique where the AI answers questions using YOUR documents instead of just its training data.

---

## 🤔 What does this app do?

1. You upload a **PDF or TXT file** (e.g. a research paper, a contract, a book chapter)
2. The app **chunks** the document into small pieces and stores them in a local vector database (ChromaDB)
3. You ask a **question** in plain English
4. The app finds the most relevant chunks and sends them to GPT — which then answers based on your document

---

## 🧠 Concepts you'll learn

| Concept | What it means |
|---|---|
| **Document Loader** | Reads a PDF/TXT file into memory |
| **Text Splitter** | Cuts the document into small chunks (~500 chars each) |
| **Embeddings** | Converts text to numbers so we can measure similarity |
| **Vector Store (ChromaDB)** | Stores and searches those numbers |
| **RetrievalQA Chain** | Retrieves relevant chunks → asks LLM → returns answer |

---

## 📁 Files

```
rag-app/
├── app.py           ← Streamlit UI (file upload + question input)
├── rag.py           ← All the RAG logic (load → chunk → embed → answer)
└── requirements.txt ← Python packages needed
```

---

## 🚀 How to run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Set your OpenAI API key**
```bash
export OPENAI_API_KEY=sk-...
```

**3. Run the app**
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🗺️ How the code flows

```
User uploads file
       ↓
app.py saves it to a temp path
       ↓
rag.py: build_index(path)
   ├── Load document (PyPDFLoader / TextLoader)
   ├── Split into chunks (RecursiveCharacterTextSplitter)
   ├── Embed chunks (OpenAIEmbeddings)
   └── Store in ChromaDB
       ↓
User asks a question
       ↓
rag.py: ask(question)
   ├── Find top-4 relevant chunks (ChromaDB retrieval)
   └── Ask GPT with those chunks as context
       ↓
Display answer in app.py
```

---

## 💡 Tips for beginners

- The `chroma_db/` folder is created automatically — it's your local vector database
- Try uploading a Wikipedia article saved as `.txt` to test quickly
- If you get a rate limit error, just wait a few seconds and try again