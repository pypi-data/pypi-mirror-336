"""Custom exceptions for the DocTools application."""


class DocToolsError(Exception):
    """Base exception for DocTools errors."""


class UnsupportedDocumentError(DocToolsError):
    """Raised when a document format is not supported."""
