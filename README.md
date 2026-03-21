#  NLP Health Information Assistant

An AI-powered assistant that helps users access **reliable public health information** using natural language queries.

The system uses **Natural Language Processing (NLP)** and **Retrieval-Augmented Generation (RAG)** to answer questions based on official health documents.

---

#  Project Objective

Many official health resources contain valuable information but are difficult for citizens to navigate.

This project aims to build a system that allows users to ask questions such as:

- *Quels sont les vaccins obligatoires pour les enfants de 0 à 6 mois au Maroc ?*
- *À quel âge administrer la première dose du vaccin contre l hépatite B ?*
- *Quelle est la période d incubation de la méningite virale ?*

The assistant retrieves information from trusted documents and generates a clear answer.

---

# System Architecture

The system follows a **Retrieval-Augmented Generation (RAG)** architecture.

User Question
     ↓
LangChain
     ↓
Retriever
     ↓
Vector DB
     ↓
Relevant Documents
     ↓
LLM
     ↓
Final Answer



Main components:

1. **LangChain** — orchestration framework for the RAG pipeline
2. **Embeddings** — Sentence Transformers / OpenAI text-embedding-3-large
3. **Vector store** — FAISS (local, fast similarity search)
4. **Retrieval** — top-k chunk retrieval 
5. **LLM** — gpt-4o-mini for answer generation
6. **Interface** — Streamlit chat UI 

---

# Technologies Used

| Technology | Role |
|------------|------|
| Python | Main programming language |
| LangChain | RAG pipeline orchestration |
| OpenAI text-embedding-3-large| Text embeddings |
| FAISS| Vector database |
| GPT-4o-mini | Pre-trained models |
| Streamlit | User interface |



