"""
embedding_generator.py
======================
Initializes the embedding model used to convert text chunks into vectors.
All other modules import from here — single source of truth for embeddings.
"""

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings # type: ignore
from dotenv import load_dotenv # type: ignore

#load_dotenv()

def get_embedding_model() -> OpenAIEmbeddings:
    """
    Load and return the OpenAI embedding model.

    Returns:
        OpenAIEmbeddings: ready-to-use embedding model
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-large",
        dimensions=1024
    )

def embed_text(text: str) -> list:
    """
    Embed a single text string into a vector.
    Useful for embedding a user query before retrieval.

    Args:
        text: the text to embed
    Returns:
        list of floats (the vector)
    """
    model = get_embedding_model()
    return model.embed_query(text)

