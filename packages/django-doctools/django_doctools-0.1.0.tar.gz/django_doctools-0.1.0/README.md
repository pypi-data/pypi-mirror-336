
# Django DocTools

A reusable Django application for document processing, analysis, and summarization using AI.

## Features

- Document summarization based on context and document type
- Smart topic generation and analysis
- Support for PDF, DOC, and DOCX files
- Multiple AI providers: Google's Gemini, OpenAI GPT models, and AWS Bedrock

## Installation

```bash
pip install django-doctools
```

## Usage

1. Add "doctools" to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...
    'doctools',
]
```

2. Configure your preferred AI provider in settings.py:

```python
# Choose your AI provider: "gemini", "openai", or "bedrock"
DOCTOOLS_AI_PROVIDER = "gemini"

# For Gemini
GEMINI_API_KEY = 'your-gemini-api-key'

# For OpenAI
OPENAI_API_KEY = 'your-openai-api-key'
OPENAI_MODEL_NAME = 'gpt-4o'  # Optional, defaults to gpt-4o

# For AWS Bedrock
BEDROCK_MODEL_ID = 'anthropic.claude-v2'
BEDROCK_AWS_REGION_NAME = 'us-east-1'
BEDROCK_AWS_ACCESS_KEY_ID = 'your-aws-access-key'
BEDROCK_AWS_SECRET_ACCESS_KEY = 'your-aws-secret-key'
```

3. Use the document processor in your views:

```python
from doctools.processors import DocumentProcessor

def process_document(request):
    context = request.POST.get('context')
    doc_type = request.POST.get('doc_type')
    topics = request.POST.getlist('topics', None)
    document = request.FILES.get('document')

    processor = DocumentProcessor()
    result = processor.process(
        document=document,
        context=context,
        doc_type=doc_type,
        topics=topics
    )

    return JsonResponse(result)
```

## Development

To contribute to this project:

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`
