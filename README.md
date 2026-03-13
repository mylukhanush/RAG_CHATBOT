# Gemini RAG Chatbot

A simple Retrieval Augmented Generation (RAG) chatbot built with Google Gemini, LangChain, and Streamlit.

## Features
- Upload PDF or TXT documents.
- Automatic text chunking and embedding generation.
- Semantic search using FAISS vector store.
- Context-aware answers based on document content.
- Chat history and source attribution.

## Requirements
- Python 3.9+
- Google API Key (for Gemini)

## Installation

1. Clone or download this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Create a `.env` file in the root directory and add your Google API Key:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

## Running the Chatbot

1. Open your terminal in the project root directory.
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open the provided URL in your browser.
4. Enter your Google API Key in the sidebar if not already set.
5. Upload a document and click "Process Document".
6. Start chatting!

## Project Structure
- `app.py`: Streamlit user interface.
- `rag_pipeline.py`: Document loading, chunking, and RAG logic.
- `embeddings.py`: Google AI embedding initialization.
- `vector_store.py`: FAISS vector database management.
- `requirements.txt`: Project dependencies.
