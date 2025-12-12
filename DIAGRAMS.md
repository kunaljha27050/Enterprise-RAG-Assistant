# 🏗️ System Architecture & UML Diagrams

## 1. High-Level Architecture
```mermaid
graph LR
    User[User] -->|Upload PDF| Frontend["Streamlit UI"]
    Frontend -->|Extract Text| Ingestion["Ingestion Engine"]
    Ingestion -->|Chunk & Embed| EmbedModel["HuggingFace Embeddings"]
    EmbedModel -->|Store Vectors| VectorDB[("FAISS Vector DB")]
    
    User -->|Ask Question| Frontend
    Frontend -->|Search Query| VectorDB
    VectorDB -->|Retrieve Context| Frontend
    Frontend -->|Context + Query| LLM["Llama 3.1 (Groq)"]
    LLM -->|Generate Answer| User

    sequenceDiagram
    actor User
    participant UI as Streamlit UI
    participant DB as Vector Database
    participant LLM as Llama 3.1 Model

    Note over User, UI: User asks a question
    User->>UI: Input: "What is the summary?"
    
    Note over UI, DB: Retrieval Phase
    UI->>DB: Search for relevant chunks (Query)
    DB-->>UI: Returns Top-3 Chunks (Context)
    
    Note over UI, LLM: Generation Phase
    UI->>LLM: Send Prompt (Context + Question)
    LLM-->>UI: Returns Generated Answer
    
    Note over UI, User: Display Phase
    UI-->>User: Displays Answer + Sources



    flowchart TD
    A[Raw PDF Document] -->|PyPDFLoader| B[Raw Text]
    B -->|Text Cleaning| C[Clean Text]
    C -->|RecursiveSplitter| D["Text Chunks (1000 tokens)"]
    D -->|Sentence-Transformers| E[Vector Embeddings]
    E -->|Indexing| F[("FAISS Database")]


    classDiagram
    class Frontend {
        +Streamlit App
        +Chat Interface
        +File Uploader
    }
    class Backend {
        +LangChain Engine
        +PDF Processor
        +Groq API Client
    }
    class DataLayer {
        +FAISS Index
        +HuggingFace Model
    }

    Frontend --> Backend : Sends Files & Queries
    Backend --> DataLayer : Stores/Retrieves Vectors
    DataLayer --> Backend : Returns Context


4.  Commit the file.

---

### **Step 2: DEPLOY NOW (The Final Step)**
Since you already have `app.py` and `requirements.txt`, you can start the deployment process **while** you add the diagrams.

1.  Go to **[share.streamlit.io](https://share.streamlit.io/)**
2.  Log in with GitHub.
3.  Click the blue **"New App"** button (top right).
4.  Click **"Use existing repo"**.
5.  Select your repository: `Enterprise-RAG-Assistant`.
    * **Branch:** `main`
    * **Main file path:** `app.py`
6.  Click **Deploy!**

**Wait about 2-3 minutes.** It will install everything and then **LAUNCH your live website**.

**Tell me when you see the "Success" screen!**
