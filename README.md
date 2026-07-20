# TrinetraAI

TrinetraAI is an open-source **agentic AI chatbot** built with **Python, FastAPI, LangGraph, LangChain, Google Gemini, Tavily, ChromaDB, and SQLite**.

It supports real-time streaming chat, document uploads, retrieval-augmented generation (RAG), web search, conversation memory, and a simple web UI.

---

## Features

- Chat with an AI agent powered by Google Gemini
- Stream responses in real time
- Upload documents such as PDF, DOCX, TXT, MD, PY, and CSV
- Use uploaded files as context through RAG
- Search the web with Tavily for current information
- Store and recall conversation history
- Simple FastAPI-based web interface

---

## Project Overview

This project combines:

- **FastAPI** for the backend server and API endpoints
- **Jinja2** for rendering the frontend UI
- **LangGraph** for agent orchestration
- **LangChain** for tools, messages, and RAG workflow
- **Google Gemini** as the LLM provider
- **Tavily** for web search
- **ChromaDB** for vector search over uploaded documents
- **SQLite** for conversation persistence

---

## Prerequisites

Make sure you have the following installed:

- Python 3.11
- pip or conda
- Git
- Google API key for Gemini
- Tavily API key for web search

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Shuklashivam123/TrinetraAI.git
```

### 2. Navigate to the project directory

```bash
cd TrinetraAI
```

### 3. Create a virtual environment

Using conda:

```bash
conda create -n trinetraai python=3.11 -y
```

### 4. Activate the virtual environment

```bash
conda activate trinetraai
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root directory.

```env
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=gemini-2.5-flash

TAVILY_API_KEY=your_tavily_api_key

LANGSMITH_TRACING=false
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=trinetraai
```

If you do not want to use LangSmith tracing, keep:

```env
LANGSMITH_TRACING=false
```

---

## Run Locally

Start the FastAPI application:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:8080
```

---

## Project Structure

```text
TrinetraAI/
│
├── app.py                  # FastAPI app and streaming chat endpoints
├── agent.py                # LangGraph agent setup and orchestration
├── database.py             # Conversation persistence
├── rag.py                  # Document ingestion and RAG pipeline
├── tools.py                # Agent tools (Web Search, Memory, RAG)
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── uploads/                # Uploaded documents
├── data/                   # SQLite database
└── chroma_db/              # ChromaDB vector database
```

---

## Usage

After running the application:

1. Open the application in your browser.
2. Start chatting with the AI assistant.
3. Upload documents to use them as context.
4. Ask questions about uploaded documents.
5. Ask current-information questions to trigger web search.
6. Continue conversations with stored chat history.

---

## Example Questions

```text
Summarize the uploaded PDF.
```

```text
Search the web for the latest AI agent news.
```

```text
Based on my uploaded document, what are the key points?
```

```text
Calculate 125 * 48 / 6.
```

---

## Notes

- Do not commit your `.env` file to GitHub.
- Keep API keys secure.
- Use `reload=True` only during development.
- Rotate API keys immediately if they are accidentally exposed.

---

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

---

## License

This project is open source. Please check the repository license for usage terms.