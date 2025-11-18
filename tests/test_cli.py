"""Tests for the CLI module."""

from click.testing import CliRunner
from lightrag_demo.cli import cli


def test_cli_help():
    """Test that CLI help works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "LightRAG Demo" in result.output
    assert "Commands:" in result.output


def test_cli_version():
    """Test that CLI version command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_info_command():
    """Test the info command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "LightRAG Demo Configuration" in result.output
    assert "Ollama Host" in result.output
    assert "Ollama Model" in result.output


def test_serve_help():
    """Test the serve command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["serve", "--help"])
    assert result.exit_code == 0
    assert "Start the FastAPI server" in result.output


def test_insert_help():
    """Test the insert command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["insert", "--help"])
    assert result.exit_code == 0
    assert "Insert text into the RAG system" in result.output


def test_query_help():
    """Test the query command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["query", "--help"])
    assert result.exit_code == 0
    assert "Query the RAG system" in result.output
    assert "--mode" in result.output
