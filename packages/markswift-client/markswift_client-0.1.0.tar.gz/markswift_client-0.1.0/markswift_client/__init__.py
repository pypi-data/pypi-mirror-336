"""
MarkSwift API Client
===================

A Python client for the MarkSwift API.

This module provides a simple interface to the MarkSwift API for converting
documents to Markdown.

Example:
    >>> from markswift_client import MarkSwiftClient
    >>> client = MarkSwiftClient(api_key="your_api_key")
    >>> job_id = client.convert_file("document.docx")
    >>> status = client.check_status(job_id)
    >>> if status["status"] == "completed":
    ...     markdown = client.fetch_markdown(job_id)
    ...     print(markdown)
"""

from .client import MarkSwiftClient, MarkSwiftError

__version__ = "0.1.0"
__all__ = ["MarkSwiftClient", "MarkSwiftError"]
