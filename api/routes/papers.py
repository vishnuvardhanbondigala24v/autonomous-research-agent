from fastapi import APIRouter, UploadFile, File, Query
from typing import List, Dict, Any
import os

from services.ingestion.parse_pdf import extract_text
from services.ingestion.chunker import chunk_text
from services.retrieval.indexer import DocumentIndex
from services.retrieval.embedder import Embedder
from services.nlp.qa import answer_question
from services.nlp.summarizer import build_followups
from services.graph.graph_client import extract_triples

router = APIRouter()

# Lazy-loaded services
INDEX = None
EMBEDDER = None

def initialize_services():
    global INDEX, EMBEDDER
    if INDEX is None:
        INDEX = DocumentIndex()
    if EMBEDDER is None:
        EMBEDDER = Embedder()

# Data folders
PAPERS_DIR = os.path.join("data", "papers")
CACHE_DIR = os.path.join("data", "cache")
os.makedirs(PAPERS_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)) -> Dict[str, Any]:
    initialize_services()
    try:
        file_path = os.path.join(PAPERS_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text(file_path)
        if not text.strip():
            return {"error": "No text extracted from PDF."}

        chunks = chunk_text(text)
        if not chunks:
            return {"error": "No chunks generated from text."}

        INDEX.add_document(file.filename, chunks)
        embeddings = EMBEDDER.encode(chunks)
        INDEX.set_embeddings(file.filename, embeddings)

        return {"message": f"Uploaded, embedded, and indexed {file.filename} with {len(chunks)} chunks"}
    except Exception as e:
        return {"error": f"Upload failed: {str(e)}"}

@router.get("/ask")
def ask_question(
    q: str = Query(...),
    docs: List[str] = Query([]),
    top_k: int = Query(5),
    min_score: float = Query(0.1),
) -> Dict[str, Any]:
    initialize_services()
    if not docs:
        return {"answer": "Please select at least one document.", "matches": {}, "follow_ups": []}

    matches = []
    match_indices: Dict[str, List[int]] = {}
    q_vec = EMBEDDER.encode_query(q)

    for doc in docs:
        chunks = INDEX.get_document_chunks(doc)
        emb = INDEX.get_embeddings(doc)
        if not chunks:
            continue
        if emb is None:
            emb = EMBEDDER.encode(chunks)
            INDEX.set_embeddings(doc, emb)

        sims = EMBEDDER.cosine_similarity_matrix_single(q_vec, emb)
        idx_scores = [(i, float(sims[i])) for i in range(len(chunks)) if sims[i] >= min_score]
        idx_scores.sort(key=lambda x: x[1], reverse=True)

        selected = idx_scores[:top_k]
        for i, score in selected:
            matches.append({"doc": doc, "index": i, "score": score, "chunk": chunks[i]})
            match_indices.setdefault(doc, []).append(i)

    context_chunks = [m["chunk"] for m in matches] if matches else [
        chunk for d in docs for chunk in INDEX.get_document_chunks(d)
    ]

    qa_result = answer_question(q, context_chunks)
    follow_ups = build_followups(q)

    return {"answer": qa_result, "matches": match_indices, "follow_ups": follow_ups}

@router.post("/graph")
def build_graph(docs: List[str] = Query([])) -> Dict[str, Any]:
    initialize_services()
    if not docs:
        return {"message": "Please provide at least one document."}

    triples_all = []
    for d in docs:
        chunks = INDEX.get_document_chunks(d)
        triples = extract_triples(chunks)
        triples_all.extend(triples)

    return {"message": f"Extracted {len(triples_all)} triples", "triples_sample": triples_all[:10]}
