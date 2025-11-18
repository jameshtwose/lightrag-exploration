"""Command-line interface for LightRAG demo."""

import click
import sys

from .api import run_server
from .rag import get_rag_service
from .config import settings


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    LightRAG Demo - A CLI tool for document querying using LightRAG with Ollama.
    
    This tool provides a simple interface to:
    - Insert documents into a RAG system
    - Query documents using natural language
    - Run a FastAPI server for web access
    """
    pass


@cli.command()
@click.option(
    "--host",
    default=None,
    help=f"Host to bind the API server (default: {settings.api_host})"
)
@click.option(
    "--port",
    default=None,
    type=int,
    help=f"Port to bind the API server (default: {settings.api_port})"
)
@click.option(
    "--reload",
    is_flag=True,
    help="Enable auto-reload for development"
)
def serve(host, port, reload):
    """Start the FastAPI server."""
    if host:
        settings.api_host = host
    if port:
        settings.api_port = port
    if reload:
        settings.api_reload = True
    
    click.echo(f"Starting LightRAG Demo API server...")
    click.echo(f"Server: http://{settings.api_host}:{settings.api_port}")
    click.echo(f"Docs: http://{settings.api_host}:{settings.api_port}/docs")
    click.echo(f"Ollama: {settings.ollama_host} (model: {settings.ollama_model})")
    
    run_server()


@cli.command()
@click.argument("text")
def insert(text):
    """
    Insert text into the RAG system.
    
    TEXT: The text to insert (can also be a file path prefixed with @)
    """
    # Check if text is a file reference
    if text.startswith("@"):
        file_path = text[1:]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            click.echo(f"Reading from file: {file_path}")
        except Exception as e:
            click.echo(f"Error reading file: {e}", err=True)
            sys.exit(1)
    
    click.echo("Inserting text into RAG system...")
    rag_service = get_rag_service()
    result = rag_service.insert_text(text)
    
    if result["status"] == "success":
        click.echo(click.style("✓ " + result["message"], fg="green"))
    else:
        click.echo(click.style("✗ Error: " + result["message"], fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.option(
    "--mode",
    default="hybrid",
    type=click.Choice(["naive", "local", "global", "hybrid"]),
    help="Query mode"
)
@click.option(
    "--context-only",
    is_flag=True,
    help="Only return context without generation"
)
def query(query, mode, context_only):
    """
    Query the RAG system.
    
    QUERY: The query string to search for
    """
    click.echo(f"Querying RAG system (mode: {mode})...")
    rag_service = get_rag_service()
    result = rag_service.query(
        query,
        mode=mode,
        only_need_context=context_only
    )
    
    if result["status"] == "success":
        click.echo("\n" + "="*80)
        click.echo(click.style("Result:", fg="cyan", bold=True))
        click.echo("="*80)
        click.echo(result["result"])
        click.echo("="*80 + "\n")
    else:
        click.echo(click.style("✗ Error: " + result["message"], fg="red"), err=True)
        sys.exit(1)


@cli.command()
def info():
    """Show configuration information."""
    click.echo(click.style("LightRAG Demo Configuration", fg="cyan", bold=True))
    click.echo("="*80)
    click.echo(f"Ollama Host:        {settings.ollama_host}")
    click.echo(f"Ollama Model:       {settings.ollama_model}")
    click.echo(f"Working Directory:  {settings.lightrag_working_dir}")
    click.echo(f"API Host:           {settings.api_host}")
    click.echo(f"API Port:           {settings.api_port}")
    click.echo("="*80)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
