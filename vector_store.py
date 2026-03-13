import os
from langchain_community.vectorstores import FAISS
from embeddings import get_embeddings

def create_vector_store(chunks, store_path="faiss_index"):
    """
    Creates a FAISS vector store from text chunks and saves it locally.
    """
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(store_path)
    return vector_store

def load_vector_store(store_path="faiss_index"):
    """
    Loads a FAISS vector store from a local path.
    """
    if not os.path.exists(store_path):
        return None
    
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        store_path, 
        embeddings, 
        allow_dangerous_deserialization=True  # Required for loading local FAISS index
    )
    return vector_store

def similarity_search(vector_store, query, k=3):
    """
    Performs a similarity search in the vector store for a given query.
    """
    docs = vector_store.similarity_search(query, k=k)
    return docs
