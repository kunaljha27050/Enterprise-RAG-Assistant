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

# --- API KEY ---
# ⚠️ For a public repo, it's safer to use st.secrets, but pasting here works for the demo.
GROQ_API_KEY = "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"

# --- CACHING RESOURCES (Speeds up Cloud Performance) ---
@st.cache_resource
def get_embedding_model():
    # This downloads the AI Brain (400MB) onto the Cloud Server
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def get_llm():
    return ChatGroq(model="llama-3.1-8b-instant", api_key=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)

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 I am running on the **Cloud**! I can process your PDFs using a real Vector Database.\n\nUpload a document to begin."}
    ]

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# --- SIDEBAR: DOCUMENT UPLOAD ---
with st.sidebar:
    st.header("📂 Knowledge Base")
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing on Cloud Server..."):
            try:
                all_texts = []
                for uploaded_file in uploaded_files:
                    # Save temp file
                    with open(uploaded_file.name, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Load and Split
                    loader = PyPDFLoader(uploaded_file.name)
                    documents = loader.load()
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    texts = text_splitter.split_documents(documents)
                    all_texts.extend(texts)

                # Create Vector Store (FAISS)
                embeddings = get_embedding_model()
                st.session_state.vector_store = FAISS.from_documents(all_texts, embeddings)

                st.success(f"✅ Successfully indexed {len(uploaded_files)} document(s)!")
                st.session_state.messages.append({"role": "assistant", "content": "I have finished reading. Ask me anything!"})

            except Exception as e:
                st.error(f"Error: {e}")

# --- MAIN CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant Response
    if st.session_state.vector_store is None:
        st.error("⚠️ Please upload a document first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Retrieve Context
                    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
                    docs = retriever.invoke(prompt)
                    context = "\n\n".join([doc.page_content for doc in docs])

                    # Generate Answer
                    full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:"
                    llm = get_llm()
                    response = llm.invoke(full_prompt)

                    # Display Answer
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})

                    # Optional: Show Sources
                    with st.expander("View Source Context"):
                        st.write(context)

                except Exception as e:
                    st.error(f"Error: {e}")
