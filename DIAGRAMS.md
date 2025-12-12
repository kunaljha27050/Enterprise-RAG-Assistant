# 🏗️ System Architecture & UML Diagrams

## 1. High-Level Architecture
This diagram represents the data flow from the user to the RAG Engine and back.

```mermaid
graph LR
    User[User] -->|Upload PDF| Frontend[Streamlit UI]
    Frontend -->|Extract Text| Ingestion[Ingestion Engine]
    Ingestion -->|Chunk & Embed| EmbedModel[HuggingFace Embeddings]
    EmbedModel -->|Store Vectors| VectorDB[(FAISS Vector DB)]
    
    User -->|Ask Question| Frontend
    Frontend -->|Search Query| VectorDB
    VectorDB -->|Retrieve Context| Frontend
    Frontend -->|Context + Query| LLM[Llama 3.1 (Groq)]
    LLM -->|Generate Answer| User
