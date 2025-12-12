import streamlit as st
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Enterprise RAG Assistant", layout="wide")
st.title("🧠 Enterprise Knowledge Assistant (Cloud Edition)")

# --- IMPORTS ---
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# --- API KEY CONFIGURATION (SECURE) ---
try:
    # This fetches the key securely from Streamlit Cloud
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    # Fallback for local testing (creates a warning if key is missing)
    st.error("⚠️ API Key not found! Please set it in Streamlit Secrets.")
    st.stop()

# --- CACHING RESOURCES ---
@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def get_llm():
    return ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 I am running on the **Cloud**! Upload a document to begin."}
    ]

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("📂 Knowledge Base")
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing on Cloud Server..."):
            try:
                all_texts = []
                for uploaded_file in uploaded_files:
                    with open(uploaded_file.name, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    loader = PyPDFLoader(uploaded_file.name)
                    documents = loader.load()
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    texts = text_splitter.split_documents(documents)
                    all_texts.extend(texts)
                
                embeddings = get_embedding_model()
                st.session_state.vector_store = FAISS.from_documents(all_texts, embeddings)
                
                st.success(f"✅ Indexed {len(uploaded_files)} document(s)!")
                st.session_state.messages.append({"role": "assistant", "content": "I have finished reading. Ask me anything!"})
            except Exception as e:
                st.error(f"Error: {e}")

# --- CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.vector_store is None:
        st.error("⚠️ Please upload a document first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
                    docs = retriever.invoke(prompt)
                    context = "\n\n".join([doc.page_content for doc in docs])
                    
                    full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:"
                    llm = get_llm()
                    response = llm.invoke(full_prompt)
                    
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                    
                    with st.expander("View Source Context"):
                        st.write(context)
                except Exception as e:
                    st.error(f"Error: {e}")
