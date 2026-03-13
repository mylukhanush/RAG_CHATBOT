import streamlit as st
import os
import tempfile
from rag_pipeline import load_and_process_document, answer_query
from vector_store import create_vector_store, load_vector_store
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Gemini RAG Chatbot", layout="wide")

st.title("🤖 Google Gemini RAG Chatbot")
st.markdown("Upload a document and ask questions based on its content.")

# Sidebar for configuration and upload
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    uploaded_file = st.file_uploader("Upload a PDF or Text file", type=["pdf", "txt"])
    
    if uploaded_file and api_key:
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                # Save uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    # Process document
                    chunks = load_and_process_document(tmp_path)
                    vector_store = create_vector_store(chunks)
                    st.success("Document processed and vector store created!")
                    st.session_state.vector_store = vector_store
                except Exception as e:
                    st.error(f"Error processing document: {e}")
                finally:
                    os.unlink(tmp_path)
        
        st.divider()
        st.header("Cache Management")
        if st.button("Clear Response Cache"):
            from rag_pipeline import cache
            cache.clear_cache()
            st.success("Cache cleared successfully!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about your document"):
    if "vector_store" not in st.session_state:
        st.error("Please upload and process a document first.")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, sources = answer_query(st.session_state.vector_store, prompt)
                    st.markdown(answer)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer
                    })
                except Exception as e:
                    st.error(f"Error generating answer: {e}")

if not api_key:
    st.warning("Please enter your Google API Key in the sidebar.")
elif "vector_store" not in st.session_state:
    st.info("Upload and process a document to start chatting.")
