# Autonomous Research Agent (minimal backend)

A minimal, working FastAPI backend for document Q&A:
- Upload PDFs
- Parse, chunk, and embed text
- Semantic search
- Answer questions with QA + summarization fallback
- Simple knowledge graph triple extraction

## Quick start
1. Create folders as per the repo structure.
2. `pip install -r requirements.txt`
3. `uvicorn api.main:app --reload --port 8000`
4. Open Swagger: http://localhost:8000/docs
5. Upload a PDF via `POST /upload`
6. Ask a question via `GET /ask?q=...&docs=your.pdf`

## Data directories
- `data/papers`: uploaded PDFs
- `data/cache`: embedding or index cache

## Notes
- Embeddings: sentence-transformers `all-MiniLM-L6-v2`
- QA: `distilbert-base-cased-distilled-squad`
- Summarization fallback used when QA confidence is low
