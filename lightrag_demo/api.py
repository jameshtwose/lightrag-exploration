"""FastAPI server for LightRAG demo."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal

from .rag import get_rag_service
from .config import settings


app = FastAPI(
    title="LightRAG Demo API",
    description="API for querying documents using LightRAG with Ollama",
    version="0.1.0"
)


class InsertRequest(BaseModel):
    """Request model for inserting text."""
    text: str = Field(..., description="Text to insert into the RAG system")


class QueryRequest(BaseModel):
    """Request model for querying."""
    query: str = Field(..., description="Query string")
    mode: Literal["naive", "local", "global", "hybrid"] = Field(
        default="hybrid",
        description="Query mode: naive, local, global, or hybrid"
    )
    only_need_context: bool = Field(
        default=False,
        description="If True, only return context without generation"
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LightRAG Demo API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "ollama_host": settings.ollama_host,
        "ollama_model": settings.ollama_model
    }


@app.post("/insert")
async def insert_text(request: InsertRequest):
    """
    Insert text into the RAG system.
    
    Args:
        request: InsertRequest containing the text to insert
        
    Returns:
        Result of the insertion
    """
    rag_service = get_rag_service()
    result = rag_service.insert_text(request.text)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


@app.post("/query")
async def query(request: QueryRequest):
    """
    Query the RAG system.
    
    Args:
        request: QueryRequest containing the query parameters
        
    Returns:
        Query results
    """
    rag_service = get_rag_service()
    result = rag_service.query(
        request.query,
        mode=request.mode,
        only_need_context=request.only_need_context
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


def run_server():
    """Run the FastAPI server."""
    import uvicorn
    uvicorn.run(
        "lightrag_demo.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
