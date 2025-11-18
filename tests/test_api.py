"""Tests for the FastAPI application."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from lightrag_demo.api import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "0.1.0"


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "ollama_host" in data
    assert "ollama_model" in data


@patch('lightrag_demo.api.get_rag_service')
def test_insert_endpoint_structure(mock_get_rag, client):
    """Test the insert endpoint structure."""
    mock_rag = Mock()
    mock_rag.insert_text.return_value = {"status": "success", "message": "Text inserted"}
    mock_get_rag.return_value = mock_rag
    
    response = client.post(
        "/insert",
        json={"text": "Test document content"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_rag.insert_text.assert_called_once_with("Test document content")


@patch('lightrag_demo.api.get_rag_service')
def test_query_endpoint_structure(mock_get_rag, client):
    """Test the query endpoint structure."""
    mock_rag = Mock()
    mock_rag.query.return_value = {"status": "success", "result": "Test result"}
    mock_get_rag.return_value = mock_rag
    
    response = client.post(
        "/query",
        json={
            "query": "What is this about?",
            "mode": "hybrid",
            "only_need_context": False
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_rag.query.assert_called_once_with(
        "What is this about?",
        mode="hybrid",
        only_need_context=False
    )


@patch('lightrag_demo.api.get_rag_service')
def test_insert_endpoint_error(mock_get_rag, client):
    """Test insert endpoint error handling."""
    mock_rag = Mock()
    mock_rag.insert_text.return_value = {"status": "error", "message": "Test error"}
    mock_get_rag.return_value = mock_rag
    
    response = client.post(
        "/insert",
        json={"text": "Test document content"}
    )
    assert response.status_code == 500


@patch('lightrag_demo.api.get_rag_service')
def test_query_endpoint_error(mock_get_rag, client):
    """Test query endpoint error handling."""
    mock_rag = Mock()
    mock_rag.query.return_value = {"status": "error", "message": "Test error"}
    mock_get_rag.return_value = mock_rag
    
    response = client.post(
        "/query",
        json={
            "query": "What is this about?",
            "mode": "hybrid"
        }
    )
    assert response.status_code == 500


@patch('lightrag_demo.api.get_rag_service')
def test_invalid_query_mode(mock_get_rag, client):
    """Test that invalid query mode is rejected."""
    # Mock the RAG service to avoid initialization
    mock_rag = Mock()
    mock_get_rag.return_value = mock_rag
    
    response = client.post(
        "/query",
        json={
            "query": "test",
            "mode": "invalid_mode"
        }
    )
    # Should get validation error
    assert response.status_code == 422
