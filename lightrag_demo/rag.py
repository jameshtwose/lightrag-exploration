"""LightRAG integration with Ollama backend."""

from pathlib import Path
from functools import partial
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed

from .config import settings


class RAGService:
    """Service for managing LightRAG operations."""

    def __init__(self):
        """Initialize the RAG service."""
        self.working_dir = Path(settings.lightrag_working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        
        # Create embedding function with specific model
        embedding_func = partial(
            ollama_embed,
            embed_model="nomic-embed-text"
        )
        
        self.rag = LightRAG(
            working_dir=str(self.working_dir),
            llm_model_func=ollama_model_complete,
            llm_model_name=settings.ollama_model,
            llm_model_kwargs={
                "host": settings.ollama_host,
                "options": {"num_ctx": 32768}
            },
            embedding_func=embedding_func,
            vector_db_storage_cls_kwargs={
                "embedding_model": "nomic-embed-text"
            }
        )

    def insert_text(self, text: str) -> dict:
        """
        Insert text into the RAG system.
        
        Args:
            text: The text to insert
            
        Returns:
            dict: Result of the insertion
        """
        try:
            self.rag.insert(text)
            return {"status": "success", "message": "Text inserted successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def query(
        self,
        query: str,
        mode: str = "hybrid",
        only_need_context: bool = False
    ) -> dict:
        """
        Query the RAG system.
        
        Args:
            query: The query string
            mode: Query mode - "naive", "local", "global", or "hybrid"
            only_need_context: If True, only return context without generation
            
        Returns:
            dict: Query results
        """
        try:
            result = self.rag.query(
                query,
                param=QueryParam(
                    mode=mode,
                    only_need_context=only_need_context
                )
            )
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Global RAG service instance
_rag_service = None


def get_rag_service() -> RAGService:
    """Get or create the global RAG service instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
