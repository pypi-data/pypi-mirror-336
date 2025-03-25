"""Document parsing utilities for extracting text from different document formats."""

import logging

import docx
import fitz  # PyMuPDF
from django.core.files.uploadedfile import UploadedFile

from .constants import ExceptionMessages
from .exceptions import UnsupportedDocumentError

logger = logging.getLogger(__name__)


class DocumentParser:
    """Base class for document parsers."""

    def __init__(self, file: UploadedFile) -> None:
        """Initialize the parser with the uploaded document file."""
        self.file = file

    def extract_text(self) -> str:
        """Extract text content from the document."""
        raise NotImplementedError(ExceptionMessages.METHOD_NOT_IMPLEMENTED.value)


class PDFParser(DocumentParser):
    """Parser for PDF documents."""

    def extract_text(self) -> str:
        """Extract text from PDF document."""
        try:
            doc = fitz.open(
                stream=self.file.read(), filetype="pdf"
            )  # Open PDF from memory
            text = "\n".join(
                page.get_text("text") for page in doc
            )  # Extract text from each page
        except Exception as e:
            logger.exception("Error parsing PDF")
            raise UnsupportedDocumentError(ExceptionMessages.PARSE_FAILED.value) from e
        else:
            return text


class DocxParser(DocumentParser):
    """Parser for DOCX documents."""

    def extract_text(self) -> str:
        """Extract text from DOCX document."""
        try:
            doc = docx.Document(self.file)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            logger.exception("Error parsing DOCX")
            raise UnsupportedDocumentError(ExceptionMessages.PARSE_FAILED.value) from e
        else:
            return text


class DocParser(DocumentParser):
    """Parser for DOC documents."""

    def extract_text(self) -> str:
        """Extract text from DOC document.

        Note: This is a simplified implementation. For production use,
        consider using a more robust DOC parser or converting to DOCX first.
        """
        # This is a placeholder - you may want to use a library like textract or
        # antiword. For now, we'll raise an error suggesting conversion to DOCX
        raise UnsupportedDocumentError(ExceptionMessages.UNSUPPORTED_DOCUMENT_DOC.value)


def get_parser_for_document(document: UploadedFile) -> DocumentParser:
    """Get the appropriate parser for a document based on file extension.

    Args:
        document: The uploaded document file

    Returns:
        An instance of the appropriate DocumentParser subclass

    Raises:
        UnsupportedDocumentError: If the document format is not supported

    """
    filename = document.name.lower()

    if filename.endswith(".pdf"):
        return PDFParser(document)
    if filename.endswith(".docx"):
        return DocxParser(document)
    if filename.endswith(".doc"):
        return DocParser(document)
    raise UnsupportedDocumentError(ExceptionMessages.UNSUPPORTED_DOCUMENT.value)
