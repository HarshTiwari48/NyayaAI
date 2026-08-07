# ⚖️ NyayaAI - AI Powered Indian Legal Assistant

NyayaAI is an AI-powered legal research assistant designed for the Indian legal system. It combines Retrieval-Augmented Generation (RAG), LangGraph agent workflows, Indian statutes, judgments, and user-uploaded legal documents to provide context-aware legal information.

> **Disclaimer:** NyayaAI provides legal information, **not legal advice**.

---

# ✨ Features

- 🤖 LangGraph Agentic Workflow
- 📚 RAG over Indian Statutes (BNS, BNSS, BSA)
- ⚖️ Indian Kanoon Judgment Retrieval
- 📄 User Document Analysis (PDF)
- 💬 Multi-turn Chat Memory
- 🧠 SQLite Checkpointer (LangGraph)
- 🔍 Context Aware Follow-up Questions
- ✅ Response Verification & Retry Pipeline
- 🚀 FastAPI REST API
- 🗂 Persistent Chroma Vector Database

---

# 🏗 Architecture

```
                 User

                   │

             FastAPI API

                   │

              LangGraph Agent

                   │

     ┌─────────────┼──────────────┐
     │             │              │
 Analyzer      Planner       User Document
     │             │           Research
     │             │
     │      ┌──────┴─────────┐
     │      │                │
Statute RAG         Judgment Retrieval
     │                │
     └────────┬───────┘
              │
         Generator
              │
         Verifier
              │
          Final Answer
```

---

# 🧠 Workflow

1. User sends a legal query.
2. Analyzer extracts:
   - Case Summary
   - Material Facts
   - Legal Issues
   - Whether legal research is required.
3. If research is required:
   - Relevant statutes are retrieved from ChromaDB.
   - Relevant judgments are fetched.
   - Uploaded documents are searched.
4. Generator combines all evidence.
5. Verifier validates the response.
6. If verification fails, the graph retries once.

---

# 🗃 Tech Stack

## AI

- Python
- FastAPI
- LangGraph
- LangChain
- Groq LLM
- ChromaDB
- HuggingFace Embeddings

## Retrieval

- BNS
- BNSS
- BSA
- Indian Kanoon API
- User Uploaded PDFs

## Memory

- SQLite Checkpointer
- Thread-based Conversation Memory

---

# 📂 Project Structure

```
AI
│
├── api/
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
│
├── app/
│   ├── core/
│   ├── graph/
│   │   ├── nodes/
│   │   ├── router.py
│   │   ├── state.py
│   │   └── graph.py
│   │
│   ├── rag/
│   ├── services/
│   ├── schemas/
│   └── tools/
│
├── uploads/
├── vector_store/
├── checkpoints.db
└── requirements.txt
```

---

# 🧩 LangGraph Nodes

## Analyzer

- Understands user intent
- Extracts facts
- Extracts legal issues
- Detects if legal research is required

---

## Planner

Creates optimized search queries for

- Statutes
- Judgments

---

## Statute Research

Retrieves relevant sections from

- Bharatiya Nyaya Sanhita (BNS)
- Bharatiya Nagarik Suraksha Sanhita (BNSS)
- Bharatiya Sakshya Adhiniyam (BSA)

---

## Judgment Research

Retrieves relevant Indian judgments.

---

## User Document Research

Uses uploaded PDF documents as the highest-priority factual evidence.

---

## Generator

Combines

- Conversation History
- User Documents
- Statutes
- Judgments

to generate the final response.

---

## Verifier

Checks

- Completeness
- Hallucinations
- Missing evidence

Retries once if necessary.

---

# 💬 Conversation Memory

NyayaAI supports thread-based conversation memory using LangGraph's SQLite Checkpointer.

Example:

```
User:
What is the punishment for sexual assault?

AI:
...

User:
Is there a bail option in this?
```

The assistant understands that "this" refers to the previous topic and performs fresh legal research while preserving conversational context.

---

# 📄 User Document Support

Users can upload legal documents such as:

- FIRs
- Complaints
- Contracts
- Notices

The uploaded document is treated as the primary source of factual information, while statutes and judgments are used only for legal reasoning.

---

# 🔍 Retrieval Priority

1. User Uploaded Documents
2. Indian Statutes
3. Judgments

---

# 📡 API Endpoints

## Health Check

```
GET /health
```

---

## Legal Analysis

```
POST /analyze
```

Body

```json
{
    "query":"What punishment is there for cheating?"
}
```

Query Parameters

```
thread_id=test123
```

---

## Analyze Uploaded Document

```
POST /analyze-with-document
```

Parameters

- thread_id
- query
- PDF File

---

# 🚀 Running Locally

## Clone

```bash
git clone <repository>
cd AI
```

---

## Install

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python -m uvicorn api.main:app --reload
```

---

# 📌 Future Improvements

- PostgreSQL Checkpointer
- Redis Caching
- Streaming Responses
- Citation Highlighting
- OCR Support
- Voice-based Legal Assistant
- Multi-language Support
- Lawyer Recommendation System
- Case Timeline Generation

---

# ⚠️ Disclaimer

NyayaAI is intended for educational and informational purposes only. It is **not** a substitute for professional legal advice. Users should consult a qualified legal practitioner before making legal decisions.

---

# 👨‍💻 Author

**Harsh Tiwari**

Built as a full-stack AI legal assistant leveraging modern LLMs, Retrieval-Augmented Generation (RAG), and LangGraph agent workflows.