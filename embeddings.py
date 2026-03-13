import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_embeddings():
    """
    Initializes and returns the Google Generative AI Embeddings model.
    Make sure GOOGLE_API_KEY is set in your environment variables.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set it in your environment variables or .env file.")
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2-preview",
        google_api_key=google_api_key
    )
    return embeddings
