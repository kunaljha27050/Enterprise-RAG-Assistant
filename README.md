# 🧠 Enterprise RAG Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![AI Model](https://img.shields.io/badge/AI-Llama_3.1-green)
![Status](https://img.shields.io/badge/Status-Active-success)

An **AI-powered Enterprise Knowledge Assistant** that allows users to chat with their documents (PDFs). It uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers with source citations.

## 🚀 Key Features

* **📄 Multi-Document Support:** Upload and process multiple PDF files simultaneously.
* **🤖 Advanced AI Reasoning:** Powered by **Llama 3.1** (via Groq) for high-quality natural language answers.
* **🔍 Vector Search Engine:** Uses **FAISS** (Facebook AI Similarity Search) and **HuggingFace Embeddings** to retrieve exact context.
* **⚡ Instant Retrieval:** Low-latency responses using optimized vector indexing.
* **🌐 Cloud-Ready:** Deployed and accessible via Streamlit Community Cloud.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM:** Llama 3.1-8b-instant (via Groq API)
* **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Vector DB:** FAISS
* **Orchestration:** LangChain
* **Deployment:** Streamlit Community Cloud

## ⚙️ Architecture

1.  **Ingestion:** PDFs are uploaded, text is extracted, and split into chunks (1000 tokens).
2.  **Embedding:** Text chunks are converted into vector embeddings using HuggingFace models.
3.  **Storage:** Vectors are stored in a local FAISS index.
4.  **Retrieval:** User queries undergo similarity search to find the top 3 most relevant chunks.
5.  **Generation:** The LLM receives the Context + Query to generate a final answer.

## 📦 Installation & Local Run

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/Enterprise-RAG-Assistant.git](https://github.com/your-username/Enterprise-RAG-Assistant.git)
    cd Enterprise-RAG-Assistant
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 📸 Screenshots

> *Upload your PDFs in the sidebar and start chatting instantly!*

## 📜 License

This project is licensed under the MIT License.

---
**Developed by Kunal Jha**
