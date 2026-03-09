#  NLP Health Information Assistant

An AI-powered assistant that helps users access **reliable public health information** using natural language queries.

The system uses **Natural Language Processing (NLP)** and **Retrieval-Augmented Generation (RAG)** to answer questions based on official health documents.

---

#  Project Objective

Many official health resources contain valuable information but are difficult for citizens to navigate.

This project aims to build a system that allows users to ask questions such as:

- *What are the symptoms of influenza?*
- *What vaccines are recommended for children?*
- *What should I do if I have influenza symptoms?*

The assistant retrieves information from trusted documents and generates a clear answer.

---

# 🏗 System Architecture

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

1. **Document Processing** (spaCy)
2. **Embeddings Generation** (Sentence Transformers)
3. **Vector Storage** (FAISS / ChromaDB)
4. **Retrieval System**
5. **Answer Generation (LLM)**
6. **Streamlit Interface**

---

# Technologies Used

| Technology | Role |
|------------|------|
| Python | Main programming language |
| spaCy | NLP preprocessing |
| LangChain | RAG pipeline orchestration |
| Sentence Transformers | Text embeddings |
| FAISS / ChromaDB | Vector database |
| HuggingFace Transformers | Pre-trained models |
| Streamlit | User interface |



