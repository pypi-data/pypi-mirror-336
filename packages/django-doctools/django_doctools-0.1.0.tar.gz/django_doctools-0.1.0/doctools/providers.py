"""AI model providers for document processing."""

import json
import logging
from abc import ABC, abstractmethod

import boto3
import google.generativeai as genai
import openai
from django.conf import settings

from .constants import ExceptionMessages

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Base class for AI model providers."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the AI provider with necessary configurations."""

    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        """Generate content using the AI model."""


class GeminiProvider(AIProvider):
    """Provider for Google's Gemini API."""

    def __init__(
        self, api_key: str | None = None, model_name: str = "gemini-pro"
    ) -> None:
        """Initialize the Gemini provider.

        Args:
            api_key: Gemini API key. If not provided, it will be loaded from settings.
            model_name: Name of the Gemini model to use.

        """
        self.api_key = api_key or getattr(settings, "GEMINI_API_KEY", None)
        self.model_name = model_name
        self.model = None

    def initialize(self) -> None:
        """Initialize the Gemini provider with API key."""
        if not self.api_key:
            raise ValueError(ExceptionMessages.API_KEY_MISSING.value)

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate_content(self, prompt: str) -> str:
        """Generate content using the Gemini model."""
        if not self.model:
            self.initialize()

        response = self.model.generate_content(prompt)
        return response.text


class OpenAIProvider(AIProvider):
    """Provider for OpenAI's GPT models."""

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "gpt-4o",
        organization: str | None = None,
    ) -> None:
        """Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key. If not provided, it will be loaded from settings.
            model_name: Name of the OpenAI model to use.
            organization: Optional organization ID for OpenAI API.

        """
        self.api_key = api_key or getattr(settings, "OPENAI_API_KEY", None)
        self.model_name = model_name or getattr(settings, "OPENAI_MODEL_NAME", "gpt-4o")
        self.organization = organization or getattr(
            settings, "OPENAI_ORGANIZATION", None
        )
        self.client = None

    def initialize(self) -> None:
        """Initialize the OpenAI provider with API key."""
        if not self.api_key:
            raise ValueError(ExceptionMessages.API_KEY_MISSING.value)

        self.client = openai.OpenAI(
            api_key=self.api_key, organization=self.organization
        )

    def generate_content(self, prompt: str) -> str:
        """Generate content using the OpenAI model."""
        if not self.client:
            self.initialize()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides accurate and concise information.",  # noqa: E501
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        return response.choices[0].message.content.strip()


class BedrockProvider(AIProvider):
    """Provider for AWS Bedrock models."""

    def __init__(
        self,
        model_id: str | None = None,
        region_name: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
    ) -> None:
        """Initialize the Bedrock provider.

        Args:
            model_id: ID of the Bedrock model to use. If not provided, it will be loaded
            from settings.
            region_name: AWS region name. If not provided, it will be loaded from
            settings.
            aws_access_key_id: AWS access key ID. If not provided, it will be loaded
            from settings.
            aws_secret_access_key: AWS secret access key. If not provided, it will be
            loaded from settings.

        """
        self.model_id = model_id or getattr(
            settings, "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
        )
        self.region_name = region_name or getattr(
            settings, "BEDROCK_AWS_REGION_NAME", "us-east-1"
        )
        self.aws_access_key_id = aws_access_key_id or getattr(
            settings, "BEDROCK_AWS_ACCESS_KEY_ID", None
        )
        self.aws_secret_access_key = aws_secret_access_key or getattr(
            settings, "BEDROCK_AWS_SECRET_ACCESS_KEY", None
        )
        self.client = None

    def initialize(self) -> None:
        """Initialize the Bedrock client."""
        kwargs = {"region_name": self.region_name, "service_name": "bedrock-runtime"}

        if self.aws_access_key_id and self.aws_secret_access_key:
            kwargs["aws_access_key_id"] = self.aws_access_key_id
            kwargs["aws_secret_access_key"] = self.aws_secret_access_key

        self.client = boto3.client(**kwargs)

    def generate_content(self, prompt: str, doc_content: str | None) -> str:
        """Generate content using the Bedrock model."""
        if not self.client:
            self.initialize()

        # Prepare the request body based on the model
        if "anthropic.claude" in self.model_id:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": doc_content,
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.2,
            }
        elif "amazon.titan" in self.model_id:
            body = {
                "inputText": prompt,
                "textGenerationConfig": {"maxTokenCount": 2000, "temperature": 0.7},
            }
        elif "ai21.j2" in self.model_id:
            body = {"prompt": prompt, "maxTokens": 2000, "temperature": 0.7}
        elif "meta.llama" in self.model_id:
            body = {"prompt": prompt, "max_gen_len": 2000, "temperature": 0.7}
        else:
            # Default format
            body = {"prompt": prompt, "max_tokens": 2000, "temperature": 0.7}

        response = self.client.invoke_model(
            modelId=self.model_id, body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())
        logger.info("Bedrock response: %s", response_body)

        # Extract the response text based on the model
        if "anthropic.claude" in self.model_id:
            return response_body.get("content", [{}])[0].get("text", "").strip()
        if "amazon.titan" in self.model_id:
            return response_body.get("results", [{}])[0].get("outputText", "")
        if "ai21.j2" in self.model_id:
            return (
                response_body.get("completions", [{}])[0]
                .get("data", {})
                .get("text", "")
            )
        if "meta.llama" in self.model_id:
            return response_body.get("generation", "")
        # Try common response formats

        return (
            response_body.get("completion", "")
            or response_body.get("generated_text", "")
            or response_body.get("output", "")
            or str(response_body)
        )


def get_ai_provider() -> AIProvider:
    """Get the configured AI provider.

    Returns:
        An initialized AIProvider instance.

    """
    provider_name = getattr(settings, "DOCTOOLS_AI_PROVIDER", "gemini").lower()

    if provider_name == "bedrock":
        return BedrockProvider()
    if provider_name == "openai":
        return OpenAIProvider()
    return GeminiProvider()
