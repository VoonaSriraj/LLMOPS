# 📚 RAG-Based Question Answering System with AWS Bedrock

A production-ready Retrieval-Augmented Generation (RAG) system that enables intelligent question-answering over PDF documents using AWS Bedrock foundation models, LangChain orchestration, and FAISS vector search.

---

## 📖 Project Overview

This project solves the problem of **context-aware document Q&A** by combining the power of large language models with semantic search. Traditional LLMs have knowledge cutoffs and cannot access private documents. This system bridges that gap by:

- **Ingesting** PDF documents and converting them into searchable vector embeddings
- **Storing** document chunks in a local FAISS vector database for fast similarity search
- **Retrieving** relevant context when users ask questions
- **Generating** accurate, context-grounded answers using AWS Bedrock's Titan models

### Why This Project Exists

LLMs excel at understanding and generating text but lack access to private or domain-specific documents. This RAG system enables organizations to:
- Build internal knowledge bases that employees can query
- Create customer support systems that answer questions from documentation
- Develop research assistants that can cite specific sources
- Enable domain-specific Q&A without fine-tuning models

### Real-World Use Cases

- **Corporate Knowledge Management**: Employees querying internal documentation, policies, and procedures
- **Academic Research**: Students and researchers asking questions about research papers
- **Legal Document Analysis**: Lawyers finding relevant case law or contract clauses
- **Technical Documentation**: Developers querying API docs, architecture guides, and technical specifications
- **Customer Support**: Automated systems answering questions from product manuals and FAQs

---

## ✨ Key Features

### Core Functionality
- **PDF Document Processing**: Automatic loading and chunking of PDF files from a designated directory
- **Semantic Embedding Generation**: Converts document chunks into high-dimensional vectors using AWS Bedrock Titan embeddings
- **Vector Store Management**: Local FAISS-based vector database for efficient similarity search
- **Context-Aware Retrieval**: Retrieves top-k most relevant document chunks based on semantic similarity
- **RAG-Based Answer Generation**: Combines retrieved context with user queries to generate accurate, cited answers
- **Interactive Web Interface**: Streamlit-based UI for document upload, vector store updates, and Q&A interactions

### Technical Features
- **AWS Bedrock Integration**: Uses Amazon Titan Embed Text v2 for embeddings and Titan Text Express v1 for generation
- **LangChain Orchestration**: Leverages LangChain's RetrievalQA chain for end-to-end RAG pipeline
- **Configurable Chunking**: Recursive character text splitting with customizable chunk size (1000) and overlap (200)
- **Similarity Search**: FAISS-based retrieval with configurable top-k results (default: 3)
- **Prompt Engineering**: Custom prompt template ensuring detailed, source-grounded responses (minimum 250 words)
- **Docker Support**: Containerized deployment ready for production environments

### Additional Components
- **Testing Utilities**: Separate modules for testing AWS Bedrock with Llama2 and Stable Diffusion models
- **Modular Architecture**: Separated ingestion and retrieval/generation logic for maintainability

---

## 🔄 How The Project Works

### End-to-End Workflow

#### 1. **Application Startup**
When you run `streamlit run app.py`:
- Streamlit initializes the web interface
- AWS Bedrock client is created using boto3 (credentials loaded from environment or AWS config)
- BedrockEmbeddings instance is initialized with `amazon.titan-embed-text-v2:0` model
- The UI displays two main sections: question input and sidebar controls

#### 2. **Document Ingestion Phase** (Triggered by "Update Vectors" button)

**Step 2.1: Document Loading**
- `data_ingestion()` function in `QA_system/ingestion.py` is called
- `PyPDFDirectoryLoader` scans the `./data` directory for PDF files
- All PDFs are loaded and converted into LangChain `Document` objects
- Each document contains page content and metadata (source file, page number)

**Step 2.2: Text Chunking**
- `RecursiveCharacterTextSplitter` processes the documents with:
  - `chunk_size=1000`: Each chunk contains approximately 1000 characters
  - `chunk_overlap=200`: Adjacent chunks share 200 characters to preserve context
- Documents are split into smaller, manageable pieces
- This chunking strategy ensures:
  - Chunks fit within embedding model context limits
  - Context is preserved across chunk boundaries
  - Retrieval can find relevant information even if it spans multiple pages

**Step 2.3: Embedding Generation**
- Each text chunk is sent to AWS Bedrock's Titan Embed Text v2 model
- The model converts text into 1024-dimensional vector embeddings
- Embeddings capture semantic meaning, allowing similarity search beyond keyword matching
- Process happens asynchronously via boto3 API calls

**Step 2.4: Vector Store Creation**
- `get_vector_store()` function creates a FAISS index from embeddings
- FAISS (Facebook AI Similarity Search) is a library for efficient similarity search
- The index maps each embedding to its corresponding text chunk and metadata
- Vector store is saved locally to `./faiss_index/` directory as:
  - `index.faiss`: Binary FAISS index file
  - `index.pkl`: Pickle file containing document metadata and mappings

#### 3. **Question Answering Phase** (Triggered by "Run LLM Query" button)

**Step 3.1: Question Input**
- User enters a question in the text input field
- Question is validated (non-empty check)

**Step 3.2: Vector Store Loading**
- Existing FAISS index is loaded from `./faiss_index/` directory
- Same embedding model (`titan-embed-text-v2:0`) must be used for consistency
- `allow_dangerous_deserialization=True` flag enables loading pickled objects

**Step 3.3: Question Embedding**
- User's question is converted to an embedding vector using the same Titan embedding model
- This embedding represents the semantic meaning of the question

**Step 3.4: Similarity Search (Retrieval)**
- FAISS performs cosine similarity search between question embedding and all document chunk embeddings
- Top 3 most similar chunks are retrieved (`search_kwargs={"k": 3}`)
- These chunks represent the most relevant context for answering the question
- Retrieval happens in-memory, making it extremely fast (milliseconds)

**Step 3.5: Context Assembly**
- Retrieved chunks are combined into a single context string
- Chunks are ordered by relevance (most similar first)
- Context is formatted with XML-like tags: `<context>...</context>`

**Step 3.6: Prompt Construction**
- Custom prompt template is filled with:
  - `{context}`: Retrieved document chunks
  - `{question}`: User's original question
- Prompt instructs the LLM to:
  - Use only the provided context
  - Provide detailed explanations (minimum 250 words)
  - Admit when information is not available
  - Avoid hallucination

**Step 3.7: LLM Generation**
- `RetrievalQA` chain sends the prompt to AWS Bedrock's Titan Text Express v1 model
- Model processes the prompt and generates a response
- Generation parameters (temperature, top_p) use model defaults
- Response is streamed back via boto3 API

**Step 3.8: Response Display**
- Generated answer is displayed in the Streamlit interface
- User sees the final answer with source-grounded information

### Data Flow Diagram

```
User Uploads PDFs
       ↓
[./data/ directory]
       ↓
PyPDFDirectoryLoader → Document Objects
       ↓
RecursiveCharacterTextSplitter → Text Chunks (1000 chars, 200 overlap)
       ↓
Bedrock Titan Embed Text v2 → Vector Embeddings (1024-dim)
       ↓
FAISS.from_documents() → Vector Index
       ↓
[Saved to ./faiss_index/]

User Asks Question
       ↓
Question Text
       ↓
Bedrock Titan Embed Text v2 → Question Embedding
       ↓
FAISS.similarity_search() → Top 3 Relevant Chunks
       ↓
Prompt Template (Context + Question)
       ↓
Bedrock Titan Text Express v1 → Generated Answer
       ↓
Streamlit UI → User Sees Response
```

---

## 🧠 System Architecture

### High-Level Architecture

The system follows a **three-tier architecture**:

1. **Presentation Layer**: Streamlit web interface for user interaction
2. **Application Layer**: LangChain orchestration and business logic
3. **Infrastructure Layer**: AWS Bedrock (AI models) and FAISS (vector storage)

### Component Interactions

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (app.py)               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │  UI Controls │         │ Question I/O │                  │
│  └──────┬───────┘         └──────┬───────┘                  │
└─────────┼────────────────────────┼───────────────────────────┘
          │                        │
          │                        │
┌─────────▼────────────────────────▼───────────────────────────┐
│              LangChain Orchestration Layer                    │
│  ┌──────────────────┐         ┌──────────────────────────┐  │
│  │  Ingestion Module│         │ RetrievalQA Chain        │  │
│  │  (ingestion.py)  │         │ (retrivalandgeneration.py)│  │
│  └────────┬─────────┘         └──────────┬───────────────┘  │
└───────────┼───────────────────────────────┼──────────────────┘
            │                               │
            │                               │
┌───────────▼───────────────┐   ┌───────────▼───────────────┐
│   AWS Bedrock Services    │   │   FAISS Vector Store      │
│                           │   │                           │
│  ┌─────────────────────┐ │   │  ┌─────────────────────┐ │
│  │ Titan Embed Text v2 │ │   │  │  Vector Index        │ │
│  │ (Embeddings)        │ │   │  │  (index.faiss)       │ │
│  └─────────────────────┘ │   │  └─────────────────────┘ │
│                           │   │                           │
│  ┌─────────────────────┐ │   │  ┌─────────────────────┐ │
│  │ Titan Text Express  │ │   │  │  Document Metadata   │ │
│  │ (Text Generation)   │ │   │  │  (index.pkl)         │ │
│  └─────────────────────┘ │   │  └─────────────────────┘ │
└───────────────────────────┘   └───────────────────────────┘
```

### Architecture Decisions

**Why FAISS over cloud vector databases?**
- **Cost**: No ongoing cloud service fees
- **Speed**: In-memory search is extremely fast
- **Simplicity**: No additional infrastructure to manage
- **Privacy**: Data never leaves local environment

**Why AWS Bedrock?**
- **Managed Service**: No model hosting or infrastructure management
- **Enterprise-Grade**: AWS security and compliance
- **Multiple Models**: Access to various foundation models (Titan, Llama2, etc.)
- **Pay-per-use**: Cost-effective for variable workloads

**Why LangChain?**
- **Abstraction**: Simplifies complex RAG pipeline orchestration
- **Modularity**: Easy to swap components (embeddings, vector stores, LLMs)
- **Best Practices**: Built-in patterns for RAG, prompt management, and chains

---

## 🧩 Tech Stack

### Frontend
- **Streamlit** (v1.x): Python-based web framework for rapid UI development
  - Enables interactive document upload and Q&A interface
  - No HTML/CSS/JavaScript required

### Backend
- **Python 3.9+**: Core programming language
- **LangChain**: Framework for building LLM applications
  - `langchain`: Core orchestration and chains
  - `langchain_community`: Community integrations (FAISS, PDF loaders)
  - `langchain_aws`: AWS Bedrock integrations
- **boto3** (v1.34.37): AWS SDK for Python
  - Bedrock runtime client for model invocations

### AI / ML
- **AWS Bedrock**: Managed foundation model service
  - **Amazon Titan Embed Text v2:0**: Text embedding model (1024 dimensions)
  - **Amazon Titan Text Express v1**: Text generation model
- **FAISS** (Facebook AI Similarity Search): Vector similarity search library
  - `faiss-cpu`: CPU-optimized version for local deployment

### Vector Database
- **FAISS**: Local, file-based vector index
  - No separate database server required
  - Fast in-memory similarity search
  - Persistent storage via `.faiss` and `.pkl` files

### Cloud / SDK
- **AWS Bedrock Runtime API**: RESTful API for model invocations
- **AWS IAM**: Authentication and authorization
- **AWS Region**: us-east-1 (configurable)

### Tools & Libraries
- **PyPDF**: PDF parsing and text extraction
- **tiktoken**: Token counting and text processing utilities
- **bs4** (BeautifulSoup4): HTML/XML parsing (used by LangChain internally)
- **Docker**: Containerization support

---

## 📂 Project Structure

```
LLMOPS/
│
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies
├── setup.py                        # Package installation configuration
├── DockerFile                      # Docker container definition
├── README.md                       # This file
│
├── QA_system/                      # Core RAG system module
│   ├── __init__.py                 # Package initialization
│   ├── ingestion.py                # Document loading, chunking, and vector store creation
│   └── retrivalandgeneration.py    # RAG chain, retrieval, and answer generation
│
├── data/                           # Input PDF documents directory
│   └── Retrieval-Augmented-Generation-for-NLP.pdf
│
├── faiss_index/                    # Generated vector store (created at runtime)
│   ├── index.faiss                 # FAISS vector index binary
│   └── index.pkl                   # Document metadata and mappings
│
├── testing_bedrock/                # AWS Bedrock testing utilities
│   ├── llama2.py                   # Llama2 model testing script
│   └── stabled_diffusion.py        # Stable Diffusion image generation testing
│
├── build/                          # Build artifacts (generated)
├── dist/                           # Distribution packages (generated)
├── LLMOPS.egg-info/                # Package metadata (generated)
├── qasystem.egg-info/              # Package metadata (generated)
└── env/                            # Python virtual environment (not in repo)
```

### Key Files Explained

- **`app.py`**: Orchestrates the Streamlit UI, handles user interactions, and coordinates between ingestion and retrieval modules
- **`QA_system/ingestion.py`**: Contains `data_ingestion()` for PDF loading/chunking and `get_vector_store()` for FAISS index creation
- **`QA_system/retrivalandgeneration.py`**: Implements `get_llama2_llm()` for LLM initialization and `get_response_llm()` for RAG chain execution
- **`data/`**: Place PDF files here for processing. The system automatically discovers and processes all PDFs in this directory
- **`faiss_index/`**: Auto-generated directory storing the vector database. Delete this to force re-indexing

---

## ⚙️ Installation & Setup

### Prerequisites

1. **Python 3.9 or higher**
   ```bash
   python --version  # Verify version
   ```

2. **AWS Account with Bedrock Access**
   - AWS account with Bedrock service enabled
   - IAM user/role with `bedrock:InvokeModel` permissions
   - Model access granted for:
     - `amazon.titan-embed-text-v2:0`
     - `amazon.titan-text-express-v1`

3. **AWS Credentials Configured**
   - Option 1: AWS CLI configuration
     ```bash
     aws configure
     ```
   - Option 2: Environment variables
     ```bash
     export AWS_ACCESS_KEY_ID=your_access_key
     export AWS_SECRET_ACCESS_KEY=your_secret_key
     export AWS_DEFAULT_REGION=us-east-1
     ```
   - Option 3: IAM role (if running on EC2/Lambda)

### Dependency Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd LLMOPS
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install the package directly:
   ```bash
   pip install -e .
   ```

### Environment Configuration

No additional environment variables are required if AWS credentials are configured via AWS CLI or IAM roles. However, you can override defaults:

```bash
export AWS_REGION=us-east-1  # Optional: specify AWS region
export AWS_PROFILE=myprofile  # Optional: use specific AWS profile
```

---

## 🚀 Running the Project

### Starting the Application

1. **Activate virtual environment** (if using one)
   ```bash
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. **Launch Streamlit app**
   ```bash
   streamlit run app.py
   ```

3. **Access the web interface**
   - Application opens automatically in your default browser
   - Default URL: `http://localhost:8501`

### Expected Behavior

1. **Initial State**
   - Main interface shows "QA with Doc using LangChain and AWS Bedrock" header
   - Question input field is empty
   - Sidebar displays "Update or Create the Vector Store" section

2. **First-Time Setup** (if `faiss_index/` doesn't exist)
   - Click "Update Vectors" button in sidebar
   - System processes all PDFs in `./data/` directory
   - Progress spinner appears during processing
   - Success message: "Vector store updated successfully!"
   - `faiss_index/` directory is created with index files

3. **Asking Questions**
   - Enter a question in the text input field
   - Click "Run LLM Query" button
   - System retrieves relevant context and generates answer
   - Answer appears below the input field
   - Success message: "Done!"

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t rag-qa-system -f DockerFile .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 -v $(pwd)/data:/app/data -v $(pwd)/faiss_index:/app/faiss_index rag-qa-system
   ```

   Note: Ensure AWS credentials are available inside the container (via environment variables or mounted credentials file).

---

## 🔐 Security & Configuration

### Credential Handling

The application uses **boto3's default credential chain**, which checks in this order:

1. **Environment Variables**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`
2. **AWS Credentials File**: `~/.aws/credentials` (or `%UserProfile%\.aws\credentials` on Windows)
3. **AWS Config File**: `~/.aws/config` (for region and profile settings)
4. **IAM Roles**: If running on EC2, Lambda, or ECS with attached IAM roles

**Best Practices**:
- Never commit credentials to version control
- Use IAM roles when possible (most secure)
- Rotate access keys regularly
- Use least-privilege IAM policies (only `bedrock:InvokeModel` permission needed)

### Data Safety Considerations

- **Local Storage**: Vector index and PDFs are stored locally. Ensure proper file system permissions.
- **No Data Transmission**: Document content is only sent to AWS Bedrock for embedding/generation. Consider data residency requirements.
- **Vector Store Security**: `faiss_index/` contains document chunks. Protect this directory if it contains sensitive information.
- **PDF Content**: PDFs in `./data/` are processed in-memory. Ensure directory permissions restrict unauthorized access.

### Required IAM Permissions

Minimum IAM policy for Bedrock access:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0",
        "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-express-v1"
      ]
    }
  ]
}
```

---

## 🤖 AI / ML Working

### Models Used

#### 1. **Amazon Titan Embed Text v2:0** (Embedding Model)
- **Purpose**: Converts text into numerical vector representations
- **Input**: Text strings (document chunks or questions)
- **Output**: 1024-dimensional floating-point vectors
- **Why Chosen**:
  - High-quality semantic embeddings optimized for retrieval
  - Managed service (no infrastructure to maintain)
  - Cost-effective per-request pricing
  - Supports up to 8,192 input tokens

#### 2. **Amazon Titan Text Express v1** (Text Generation Model)
- **Purpose**: Generates human-like text responses based on prompts
- **Input**: Prompt template with context and question
- **Output**: Natural language answer
- **Why Chosen**:
  - Strong performance on question-answering tasks
  - Supports long context windows
  - Fast inference times
  - Managed by AWS (no model hosting required)

### Retrieval-Augmented Generation (RAG) Flow

RAG combines **information retrieval** with **text generation**:

1. **Retrieval Phase**:
   - User question → Embedding → Similarity search in vector store
   - Returns top-k most relevant document chunks
   - This ensures the LLM has access to accurate, up-to-date information

2. **Augmentation Phase**:
   - Retrieved chunks are formatted into a prompt
   - Prompt explicitly instructs the model to use only provided context
   - This prevents hallucination and ensures source-grounded answers

3. **Generation Phase**:
   - LLM processes the augmented prompt
   - Generates answer based on retrieved context
   - Response is more accurate than pure LLM generation because it's grounded in source material

### Why RAG Over Fine-Tuning?

- **No Training Required**: Works immediately with new documents
- **Source Attribution**: Can trace answers back to specific document chunks
- **Updatable Knowledge**: Add new documents without retraining
- **Cost-Effective**: No GPU training infrastructure needed
- **Domain Flexibility**: Works across any domain without model modification

### Limitations

1. **Context Window**: Limited by LLM's maximum context length. Very long documents may require more sophisticated chunking or summarization.
2. **Retrieval Quality**: Answer quality depends on retrieval accuracy. If relevant chunks aren't retrieved, the answer may be incomplete.
3. **Chunking Artifacts**: Information split across chunk boundaries may be lost if overlap is insufficient.
4. **Model Limitations**: Inherits limitations of Titan Text Express (e.g., knowledge cutoff, potential biases).
5. **Local Storage**: FAISS index size grows with document count. Very large corpora may require cloud vector databases.
6. **Single Document Type**: Currently supports only PDFs. Other formats (Word, HTML, etc.) require additional loaders.

---

## ⚠️ Limitations & Known Issues

### Current Limitations

1. **PDF-Only Support**: Only processes PDF files. Other document formats require code modifications.
2. **Local Vector Store**: FAISS index is stored locally, limiting scalability and multi-user access.
3. **No Conversation History**: Each question is treated independently. No multi-turn conversation support.
4. **Fixed Chunking Strategy**: Chunk size (1000) and overlap (200) are hardcoded. May not be optimal for all document types.
5. **No Source Citations**: Answers don't explicitly cite which document chunks were used (though metadata is available).
6. **Single Region**: AWS region is hardcoded to `us-east-1` in ingestion module.
7. **No Error Recovery**: If Bedrock API fails, the application may crash without graceful error handling.
8. **Synchronous Processing**: Document ingestion blocks the UI. Large document sets may cause timeouts.

### Known Issues

- **Model ID Inconsistency**: `app.py` defines `get_llama2_llm()` locally, but also imports it from `retrivalandgeneration.py`. The local definition takes precedence, which may cause confusion.
- **Typo in Filename**: `retrivalandgeneration.py` should be `retrievalandgeneration.py` (missing 'e' in retrieval).
- **Dangerous Deserialization**: FAISS loading uses `allow_dangerous_deserialization=True`, which poses security risks if index files are from untrusted sources.

---

## 🔮 Future Improvements

### Short-Term Enhancements

1. **Multi-Format Support**: Add loaders for Word documents, HTML, Markdown, and plain text files.
2. **Configurable Chunking**: Make chunk size and overlap configurable via UI or config file.
3. **Source Citation**: Display which document chunks were used to generate each answer.
4. **Error Handling**: Add try-catch blocks and user-friendly error messages for API failures.
5. **Progress Indicators**: Show detailed progress during document ingestion (e.g., "Processing document 3 of 10").
6. **Conversation History**: Implement session-based conversation memory for follow-up questions.

### Medium-Term Enhancements

1. **Cloud Vector Database**: Migrate to AWS OpenSearch, Pinecone, or Weaviate for scalable, multi-user access.
2. **Advanced Retrieval**: Implement hybrid search (keyword + semantic), reranking, and query expansion.
3. **Multiple LLM Support**: Allow users to choose between different Bedrock models (Claude, Llama2, etc.).
4. **Batch Processing**: Support bulk question answering and export results to CSV/JSON.
5. **Authentication**: Add user authentication and authorization for enterprise deployments.
6. **Monitoring**: Integrate CloudWatch for logging, metrics, and cost tracking.

### Long-Term Enhancements

1. **Multi-Modal RAG**: Support images, tables, and charts in documents.
2. **Fine-Tuning Integration**: Option to fine-tune embedding models on domain-specific data.
3. **Agentic RAG**: Implement LangChain agents for complex, multi-step queries.
4. **Streaming Responses**: Stream LLM responses token-by-token for better UX.
5. **Evaluation Framework**: Add RAG evaluation metrics (retrieval accuracy, answer quality, etc.).
6. **API Endpoints**: Expose REST API for programmatic access and integration with other systems.

---

## 📜 License

This project does not specify a license in the codebase. Please add an appropriate license file (e.g., MIT, Apache 2.0) based on your intended use case.

**Note**: Ensure compliance with:
- AWS Bedrock Terms of Service
- LangChain license (MIT)
- FAISS license (MIT)
- Streamlit license (Apache 2.0)

---

## 🗣️ Interview Explanation Section

### 30-Second Explanation

"This is a RAG (Retrieval-Augmented Generation) system that answers questions from PDF documents. Users upload PDFs, which are chunked and converted into vector embeddings using AWS Bedrock. These embeddings are stored in a FAISS vector database. When users ask questions, the system retrieves the most relevant document chunks and passes them to an LLM to generate accurate, source-grounded answers. It's built with LangChain, Streamlit, and AWS Bedrock."

### 2-Minute Explanation

"This project implements a production-ready RAG system for document question-answering. Here's how it works:

**Architecture**: The system has three main components - a Streamlit frontend, LangChain orchestration layer, and AWS Bedrock for AI models.

**Document Processing**: When documents are uploaded, the system uses PyPDF to extract text, then splits documents into 1000-character chunks with 200-character overlap. Each chunk is embedded using AWS Bedrock's Titan Embed Text model, creating 1024-dimensional vectors that capture semantic meaning.

**Vector Storage**: These embeddings are stored in a local FAISS index, which enables fast similarity search. FAISS was chosen for its speed and because it doesn't require a separate database server.

**Question Answering**: When a user asks a question, the question is also embedded, and FAISS finds the top 3 most semantically similar document chunks. These chunks are combined with the question in a prompt template and sent to AWS Bedrock's Titan Text Express model, which generates a detailed answer grounded in the retrieved context.

**Why RAG?**: This approach solves the problem of LLMs having outdated knowledge or lacking access to private documents. By retrieving relevant context first, we ensure answers are accurate and traceable to source material.

**Tech Choices**: I used LangChain for orchestration because it provides battle-tested RAG patterns, AWS Bedrock for managed model access, and Streamlit for rapid UI development. The system is containerized with Docker for easy deployment."

### Key Talking Points for Interviews

1. **RAG Architecture Understanding**
   - Explain why retrieval before generation improves answer quality
   - Discuss trade-offs between RAG and fine-tuning
   - Mention how chunking strategy affects retrieval quality

2. **Vector Search Expertise**
   - Explain how semantic embeddings enable similarity search beyond keywords
   - Discuss why FAISS was chosen (speed, simplicity) and when you'd use cloud alternatives
   - Mention cosine similarity and how it measures semantic relatedness

3. **AWS Bedrock Integration**
   - Demonstrate understanding of managed AI services vs. self-hosted models
   - Explain embedding models vs. text generation models and their different roles
   - Discuss cost considerations and when to use different Bedrock models

4. **LangChain Proficiency**
   - Explain how LangChain abstracts complex RAG pipelines
   - Discuss RetrievalQA chain and its components (retriever, LLM, prompt)
   - Mention how LangChain enables swapping components (e.g., different vector stores)

5. **Production Considerations**
   - Discuss scalability limitations of local FAISS and migration paths
   - Explain error handling and monitoring needs
   - Mention security considerations (credentials, data privacy)

6. **Problem-Solving Approach**
   - Explain how you'd handle very long documents (hierarchical chunking, summarization)
   - Discuss improving retrieval quality (reranking, hybrid search)
   - Mention evaluation strategies (retrieval metrics, answer quality metrics)

---

**Built with ❤️ using LangChain, AWS Bedrock, and Streamlit**

