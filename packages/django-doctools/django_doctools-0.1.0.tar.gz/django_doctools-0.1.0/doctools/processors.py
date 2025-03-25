"""Core document processing functionality."""

import base64
import io
import logging
from typing import Any

import fitz
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
from pydantic import BaseModel, Field

from .constants import ExceptionMessages
from .exceptions import DocToolsError
from .parsers import get_parser_for_document
from .providers import AIProvider, get_ai_provider

logger = logging.getLogger(__name__)


class Topic(BaseModel):
    """A topic extracted from or provided for a document."""

    title: str
    summary: str = ""
    citations: list[dict[str, Any]] = Field(default_factory=list)


class DocumentAnalysis(BaseModel):
    """Results of document analysis and summarization."""

    topics: list[Topic]
    context: str
    document_type: str


class DocumentProcessor:
    """Main processor for document analysis and summarization."""

    def __init__(self, ai_provider: AIProvider = None) -> None:
        """Initialize the document processor.

        Args:
            ai_provider: Optional AI provider instance. If not provided, it will be
            loaded using get_ai_provider().

        """
        try:
            self.ai_provider = ai_provider or get_ai_provider()
            self.ai_provider.initialize()
        except Exception as e:
            logger.exception("Failed to initialize AI provider")
            raise DocToolsError(ExceptionMessages.AI_PROVIDER_INIT_FAILED.value) from e

    def pdf_to_base64(self, pdf_file: UploadedFile) -> bytes:
        """Convert a multi-page PDF into a single concatenated base64-encoded image."""
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()  # Read PDF file as bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")  # Load PDF from memory

        images = []
        for page in doc:
            pix = page.get_pixmap()  # Render page as an image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

        # Get max width and total height for final image
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)

        # Create blank image to merge all pages
        merged_image = Image.new("RGB", (max_width, total_height), "white")

        # Paste images one below another
        y_offset = 0
        for img in images:
            merged_image.paste(img, (0, y_offset))
            y_offset += img.height

        # Convert merged image to base64
        image_bytes = io.BytesIO()
        merged_image.save(image_bytes, format="PNG")
        return base64.b64encode(image_bytes.getvalue()).decode("utf-8")

    def process(
        self,
        document: UploadedFile,
        context: str,
        doc_type: str,
    ) -> DocumentAnalysis:
        """Process a document to extract summaries based on topics.

        Args:
            document: The uploaded document file
            context: The context of the document (e.g., legal, financial)
            doc_type: The type of the document within the context
            topics: Optional list of topics to extract information for

        Returns:
            DocumentAnalysis object with extracted information

        """
        try:
            # Get appropriate parser for the document
            parser = get_parser_for_document(document)
            if document.name.lower().endswith(".pdf"):
                doc_content = self.pdf_to_base64(document)
            else:
                doc_content = parser.extract_text()

            summary = self._generate_summary(doc_content, context, doc_type)

            # TODO(Anshuman):
            # return DocumentAnalysis(
            #     topics=processed_topics, context=context, document_type=doc_type
            # )

        except Exception as e:
            logger.exception("Error processing document")
            raise DocToolsError(
                ExceptionMessages.DOCUMENT_PROCESSING_FAILED.value
            ) from e

        else:
            return summary

    def _generate_summary(self, doc_content: str, context: str, doc_type: str) -> str:
        """Generate a summary of the document content."""
        prompt = f"""
        You are an expert in {context} documents, particularly {doc_type} documents.
        Analyse the following document and extract key information with citations to the
        original text. Make sure that the provided analysis is accurate and relevant to
        the context. Group the analysis under various topics that are oftne used and
        known to the experts in the {context} domain. The goal is to provide a concise
        summary of the document content under each of these topics.

        ANALYSIS REQUIREMENTS:
        1. Extract information into a structured JSON format
        2. Provide specific citations for each piece of extracted information
        3. Maintain consistent depth of analysis across all sections
        4. Flag missing standard elements and unusual provisions

        OUTPUT STRUCTURE:
        Return a JSON object with the following structure:
        [{{"topic": "exact topic here","type": "information","summary": "summary here","citation": "exact page and line no. or section or coordinates if it's a PDF"}}]

        Also append an overall summary of the document content in upto 200 words in the
        structure below:
        [{{"topic": "Overall Summary","type": "summary","summary": "summary here","citation": "None"}}]

        If it's a legal document, then identify risks and append those risks in the
        format below:
        [{{"topic": "Add a very short one-line description of the risk here","type": "risk","summary": "summary here","remediation": "suggest remediation here","citation": "exact page, line no. or section or coordinates if it's a PDF"}}]

        For each field, provide accurate information extracted from the document with
        appropriate citations.
        If information is not available in the document under a specific topic which you
        think should be present under the {context} domain and {doc_type} document type,
        use "Not specified" as the value.

        Don't add any space characters anywhere like \\n or \\t in the JSON output.
        """  # noqa: E501
        logger.info("Prompt generated: %s", prompt)

        return self.ai_provider.generate_content(prompt, doc_content).strip()
