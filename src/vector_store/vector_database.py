import sys
from pathlib import Path

# Adds src/ to the path so Python can find embeddings/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from langchain_community.vectorstores import FAISS # type: ignore
from embeddings.embedding_generator import get_embedding_model
from langchain_core.documents import Document  # type: ignore
import json


if __name__ == "__main__":
    
    # Load the cleaned chunks from the json files
    documents = []
    for source in [
        "source_1",
        "source_2",
        "source_3",
        "source_4",
        "source_5"]:
        
        with open(f"data/preprossed/cleaned/chunks_{source}.json  ", "r", encoding="utf-8") as f:
            documents.append(json.load(f))


    # convert the list of lists of dicts into a list of Document objects
    chunks = []
    for document in documents:
        for element in document:
            chunk = Document(
                page_content=element["page_content"],
                metadata= element["metadata"])
            chunks.append(chunk)
            

    # Create the embedding model
    embedding_model = get_embedding_model()


    # Create the FAISS vector store
    vector_store = FAISS.from_documents(chunks, embedding_model)

    # Save the vector store to disk
    vector_store.save_local("data/faiss_vector_store")