import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# --- PAGE CONFIG ---
st.set_page_config(page_title="Enterprise RAG Global", layout="wide")
st.title("🌍 Enterprise Knowledge Assistant (Global Cloud)")

# --- API KEY (SECURE) ---
try:
    # Fetches key from Streamlit Cloud Secrets
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("⚠️ API Key missing! Go to App Settings -> Secrets to add it.")
    st.stop()

# --- CACHING ---
@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def get_llm():
    return ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 I am Online! Upload a PDF to chat."}]

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("📂 Upload Docs")
    uploaded_files = st.file_uploader("Choose PDF", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files and st.button("Process"):
        with st.spinner("Processing on Cloud..."):
            try:
                all_texts = []
                for uploaded_file in uploaded_files:
                    with open(uploaded_file.name, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    loader = PyPDFLoader(uploaded_file.name)
                    docs = loader.load()
                    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    texts = splitter.split_documents(docs)
                    all_texts.extend(texts)
                
                embeddings = get_embedding_model()
                st.session_state.vector_store = FAISS.from_documents(all_texts, embeddings)
                st.success(f"✅ Indexed {len(uploaded_files)} files!")
            except Exception as e:
                st.error(f"Error: {e}")

# --- CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not st.session_state.vector_store:
        st.error("⚠️ Upload a PDF first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
                    docs = retriever.invoke(prompt)
                    context = "\n\n".join([d.page_content for d in docs])
                    
                    llm = get_llm()
                    response = llm.invoke(f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:")
                    
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                except Exception as e:
                    st.error(f"Error: {e}")
