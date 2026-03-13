import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from embeddings import get_embeddings
from vector_store import create_vector_store, load_vector_store

from cache_manager import CacheManager

cache = CacheManager()

def load_and_process_document(file_path):
    """
    Loads a PDF or TXT file, splits it into chunks, and returns the chunks.
    """
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    
    documents = loader.load()
    
    # Text chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def generate_answer(llm, context, question):
    """
    Generates an answer using the LLM and the provided context.
    """
    template = """You are a helpful assistant. Use the provided context to answer the user's question accurately.
    If the answer is not contained within the context, politely say that you don't know based on the document, but try your best to find relevant mentions (e.g., names, totals, specific details).

    Context:
    {context}
    
    Question: {question}
    
    Helpful Answer:"""
    
    prompt = PromptTemplate(
        template=template, 
        input_variables=["context", "question"]
    )
    
    # Format the prompt
    formatted_prompt = prompt.format(context=context, question=question)
    
    # Invoke the LLM
    response = llm.invoke(formatted_prompt)
    return response.content

def answer_query(vector_store, query):
    """
    Answers a query by manually retrieving context and calling the LLM with caching.
    """
    # 1. Check cache first
    cached_answer, cached_sources = cache.get_cached_response(query)
    if cached_answer:
        return cached_answer, cached_sources

    # 2. Retrieve relevant documents
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    
    # 3. Combine context
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # 4. Initialize LLM
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0
    )
    
    # 5. Generate answer
    answer = generate_answer(llm, context, query)
    
    # 6. Store in cache
    cache.cache_response(query, answer, docs)
    
    return answer, docs
