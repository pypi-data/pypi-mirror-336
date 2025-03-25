"""Constants used in the doctools package."""

from enum import Enum


class ExceptionMessages(Enum):
    """Exception messages."""

    METHOD_NOT_IMPLEMENTED = "Subclasses must implement extract_text method"
    PARSE_FAILED = "Failed to parse the document"
    UNSUPPORTED_DOCUMENT_DOC = (
        "DOC format is not directly supported. Please convert to DOCX and try again."
    )
    UNSUPPORTED_DOCUMENT = "Unsupported document format. Use DOCX or PDF."
    AI_PROVIDER_INIT_FAILED = "Failed to initialize AI provider"
    DOCUMENT_PROCESSING_FAILED = "Failed to process the document"
    API_KEY_MISSING = "API key is missing"
