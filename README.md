# lightrag-exploration

A command-line demo application that uses LightRAG for Retrieval-Augmented Generation (RAG) with local AI via Ollama, served through a FastAPI web interface.

## Features

- 🚀 **CLI Interface**: Easy-to-use command-line tool installable via pipx
- 📚 **LightRAG**: Advanced RAG system for document querying
- 🤖 **Local AI**: Uses Ollama for local LLM inference
- 🌐 **FastAPI Server**: RESTful API for web-based access
- ⚙️ **Pydantic Settings**: Configuration management using environment variables
- 📦 **Poetry**: Modern Python dependency management

## Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running locally
- Poetry (for development) or pipx (for installation)

## Installation

### Using pipx (Recommended for end users)

```bash
pipx install lightrag-demo
```

### Using Poetry (For development)

```bash
# Clone the repository
git clone https://github.com/jameshtwose/lightrag-exploration.git
cd lightrag-exploration

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Configuration

Create a `.env` file in your working directory (see `.env.example` for reference):

```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# LightRAG Configuration
LIGHTRAG_WORKING_DIR=./lightrag_cache

# FastAPI Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false
```

## Ollama Setup

1. Install Ollama from https://ollama.ai/
2. Pull the required models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

3. Ensure Ollama is running:

```bash
ollama serve
```

## Usage

### Command-Line Interface

#### View available commands:

```bash
lightrag-demo --help
```

#### Start the API server:

```bash
lightrag-demo serve
```

With custom host and port:

```bash
lightrag-demo serve --host 127.0.0.1 --port 3000
```

With auto-reload for development:

```bash
lightrag-demo serve --reload
```

#### Insert text into the RAG system:

```bash
lightrag-demo insert "Your text content here"
```

Insert from a file:

```bash
lightrag-demo insert @path/to/document.txt
```

#### Query the RAG system:

```bash
lightrag-demo query "What is this document about?"
```

With different query modes:

```bash
lightrag-demo query "Your question" --mode local
lightrag-demo query "Your question" --mode global
lightrag-demo query "Your question" --mode hybrid
```

Get only context without generation:

```bash
lightrag-demo query "Your question" --context-only
```

#### Show configuration:

```bash
lightrag-demo info
```

### API Server

Once the server is running, you can:

- View API documentation at `http://localhost:8000/docs`
- Access the interactive API at `http://localhost:8000/redoc`

#### API Endpoints:

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /insert` - Insert text into the RAG system
- `POST /query` - Query the RAG system

#### Example API requests:

**Insert text:**

```bash
curl -X POST "http://localhost:8000/insert" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document content here"}'
```

**Query:**

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this about?",
    "mode": "hybrid",
    "only_need_context": false
  }'
```

## Development

### Install development dependencies:

```bash
poetry install
```

### Run tests:

```bash
poetry run pytest
```

### Format code:

```bash
poetry run black lightrag_demo/
poetry run isort lightrag_demo/
```

### Type checking:

```bash
poetry run mypy lightrag_demo/
```

## Query Modes

LightRAG supports four query modes:

- **naive**: Simple retrieval without graph structure
- **local**: Focus on local context and relationships
- **global**: Consider global document structure
- **hybrid**: Combine local and global approaches (recommended)

## Troubleshooting

### Ollama connection issues:

- Ensure Ollama is running: `ollama serve`
- Check the Ollama host in your `.env` file
- Verify models are pulled: `ollama list`

### Permission errors:

- Ensure the `LIGHTRAG_WORKING_DIR` is writable
- Check file permissions for the cache directory

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

