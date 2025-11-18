"""Tests for configuration module."""

import os
from lightrag_demo.config import Settings


def test_settings_defaults():
    """Test that settings have correct default values."""
    settings = Settings()
    
    assert settings.ollama_host == "http://localhost:11434"
    assert settings.ollama_model == "llama3.2"
    assert settings.lightrag_working_dir == "./lightrag_cache"
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8000
    assert settings.api_reload is False


def test_settings_from_env(monkeypatch):
    """Test that settings can be loaded from environment variables."""
    monkeypatch.setenv("OLLAMA_HOST", "http://custom-host:8080")
    monkeypatch.setenv("OLLAMA_MODEL", "custom-model")
    monkeypatch.setenv("API_PORT", "9000")
    
    settings = Settings()
    
    assert settings.ollama_host == "http://custom-host:8080"
    assert settings.ollama_model == "custom-model"
    assert settings.api_port == 9000
