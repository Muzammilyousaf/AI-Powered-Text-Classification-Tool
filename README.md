# AI-Powered Text Classification Tool

A production-ready Python tool for classifying text into predefined categories using **OpenAI's LLM API** (GPT-3.5-turbo/GPT-4). Supports single text and batch processing with deterministic, configurable prompts.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Python API](#python-api-usage)
- [Examples](#example-test-cases)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Cost Considerations](#cost-considerations)

## Features

- ✅ **AI-Powered Classification**: Uses OpenAI API (GPT-3.5-turbo or GPT-4) for accurate text classification
- ✅ **Web UI**: Beautiful, modern web interface for easy text classification
- ✅ **Command-Line Interface**: Full-featured CLI for automation and scripting
- ✅ **Deterministic Prompts**: Consistent, repeatable classification results
- ✅ **Configurable Labels**: Customize classification categories via config file or command-line
- ✅ **Batch Processing**: Process multiple texts efficiently
- ✅ **File Upload**: Support for TXT and JSON file uploads
- ✅ **Structured JSON Output**: Includes predicted label, confidence score, and rationale
- ✅ **Production-Ready**: Error handling, validation, and comprehensive documentation

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- pip (Python package manager)

### Setup

1. **Clone or download this project**

```bash
git clone <repository-url>
cd text-classifier
```

Or download and extract the project files.

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Configure API key**:

**Option A: Using .env file (Recommended)**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Option B: Environment variable**
```bash
# Linux/Mac
export OPENAI_API_KEY=sk-your-actual-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"

# Windows (CMD)
set OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Quick Start

### Command Line Usage

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key (see Installation above)

# 3. Classify a single text
python text_classifier.py "I'm unhappy with the service"

# 4. Run test examples
python test_examples.py
```

### Web UI Usage

```bash
# 1. Install dependencies (includes Flask)
pip install -r requirements.txt

# 2. Set your API key in .env file

# 3. Run the web UI
python run_ui.py
# Or: python app.py

# 4. Open your browser to: http://localhost:5000
```

The web UI provides:
- ✅ Single text classification
- ✅ Batch text processing
- ✅ File upload (TXT or JSON)
- ✅ Visual results with confidence scores
- ✅ Download results as JSON
- ✅ Statistics and analytics

## Usage

### Single Text Classification

```bash
python text_classifier.py "I'm very unhappy with the service I received yesterday"
```

**Output**:
```json
[
  {
    "text": "I'm very unhappy with the service I received yesterday",
    "predicted_label": "Complaint",
    "confidence": 0.95,
    "rationale": "The text expresses clear dissatisfaction with a service experience."
  }
]
```

### Batch Processing from File

Create a file `input.txt` with one text per line:
```
What are your business hours?
I love your new product design!
The delivery was late and damaged.
```

Then run:
```bash
python text_classifier.py --file input.txt
```

### JSON Array Input

Create `input.json`:
```json
[
  "What are your business hours?",
  "I love your new product design!",
  "The delivery was late and damaged."
]
```

```bash
python text_classifier.py --file input.json
```

### Save Output to File

```bash
python text_classifier.py --file input.txt --output results.json
```

### Interactive Mode

Run without arguments for interactive mode:
```bash
python text_classifier.py
```

### Custom Configuration

Use a custom config file with different labels:
```bash
python text_classifier.py "Your text here" --config custom_config.json
```

### Custom Labels via Command Line

```bash
python text_classifier.py "Your text" --labels "Positive" "Negative" "Neutral"
```

### Using Different Models

```bash
python text_classifier.py "Your text" --model gpt-4
```

## Configuration File Format

Create a `config.json` file to customize labels and prompts:

```json
{
  "labels": ["Complaint", "Inquiry", "Feedback", "Other"],
  "prompt_template": "Your custom prompt template here. Use {labels} and {text} as placeholders."
}
```

## Python API Usage

You can also use the classifier as a Python library:

```python
from text_classifier import TextClassifier

# Initialize classifier
classifier = TextClassifier(
    api_key="your-api-key",  # or set OPENAI_API_KEY env var
    model="gpt-3.5-turbo",
    labels=["Complaint", "Inquiry", "Feedback", "Other"]
)

# Classify single text
result = classifier.classify("I need help with my account")
print(f"Label: {result.predicted_label}")
print(f"Confidence: {result.confidence}")
print(f"Rationale: {result.rationale}")

# Batch classification
texts = [
    "What are your hours?",
    "I'm very disappointed",
    "Great service!"
]
results = classifier.classify_batch(texts)
for result in results:
    print(f"{result.text} -> {result.predicted_label}")
```

## Example Test Cases

### Test Inputs

1. **Complaint**: "I'm very unhappy with the service I received yesterday. The staff was rude and unhelpful."
2. **Inquiry**: "What are your business hours? Do you offer weekend service?"
3. **Feedback**: "I love your new product design! The user interface is much more intuitive now."
4. **Other**: "The weather is nice today."

### Expected Outputs

```json
[
  {
    "text": "I'm very unhappy with the service I received yesterday. The staff was rude and unhelpful.",
    "predicted_label": "Complaint",
    "confidence": 0.98,
    "rationale": "The text clearly expresses dissatisfaction and negative experiences with service and staff."
  },
  {
    "text": "What are your business hours? Do you offer weekend service?",
    "predicted_label": "Inquiry",
    "confidence": 0.95,
    "rationale": "The text contains direct questions seeking information about business operations."
  },
  {
    "text": "I love your new product design! The user interface is much more intuitive now.",
    "predicted_label": "Feedback",
    "confidence": 0.92,
    "rationale": "The text provides positive feedback and constructive comments about product improvements."
  },
  {
    "text": "The weather is nice today.",
    "predicted_label": "Other",
    "confidence": 0.85,
    "rationale": "The text does not fit into complaint, inquiry, or feedback categories."
  }
]
```

## Output Format

Each classification result includes:

- **text**: The original input text
- **predicted_label**: The classified category (one of the configured labels)
- **confidence**: Optional confidence score (0.0 to 1.0)
- **rationale**: Optional explanation of the classification
- **error**: Optional error message if classification failed

## Error Handling

The tool handles various error scenarios:

- Missing API key: Clear error message with setup instructions
- Invalid API responses: Graceful fallback with error details
- Network issues: Error messages in output
- Invalid labels: Validation with helpful error messages

## Deterministic Classification

The tool uses:
- `temperature=0.0` for deterministic outputs
- Structured JSON response format
- Consistent prompt templates
- Label validation to ensure outputs match configured categories

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.0015 per 1K tokens (very cost-effective)
- **GPT-4**: ~$0.03 per 1K tokens (higher accuracy, more expensive)
- Each classification uses ~100-200 tokens

## Troubleshooting

### "OpenAI API key not found"
- Ensure `.env` file exists with `OPENAI_API_KEY` set
- Or export the environment variable: `export OPENAI_API_KEY=your-key`

### "Invalid label" errors
- Ensure labels in config match exactly (case-sensitive)
- Check that the prompt template includes proper label instructions

### JSON parsing errors
- The tool automatically handles markdown code blocks
- If issues persist, check OpenAI API response format

## Project Structure

```
text-classifier/
├── text_classifier.py      # Main classification script
├── config.json             # Default configuration (labels & prompts)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── test_examples.py        # Test script with examples
├── example_input.txt      # Sample input file for testing
├── .env.example          # Environment variable template
└── .gitignore            # Git ignore file
```

## Command-Line Options

```bash
python text_classifier.py [OPTIONS] [TEXT]

Arguments:
  TEXT                    Text to classify (optional if using --file)

Options:
  --file FILE             Path to file with texts (one per line or JSON array)
  --config FILE           Path to custom configuration JSON file
  --model MODEL           OpenAI model to use (default: gpt-3.5-turbo)
  --output FILE           Output file path (default: stdout)
  --labels LABEL [LABEL] Custom labels (overrides config file)
  -h, --help             Show help message
```

## Advanced Usage

### Custom Prompt Templates

Create a custom `config.json`:

```json
{
  "labels": ["Urgent", "Normal", "Low Priority"],
  "prompt_template": "Classify this customer message into priority levels: {labels}\n\nMessage: \"{text}\"\n\nRespond with JSON: {\"label\": \"...\", \"confidence\": 0.0-1.0, \"rationale\": \"...\"}"
}
```

### Using with Different Models

```bash
# Use GPT-4 for higher accuracy (more expensive)
python text_classifier.py "Your text" --model gpt-4

# Use GPT-3.5-turbo (default, cost-effective)
python text_classifier.py "Your text" --model gpt-3.5-turbo
```

### Processing Large Batches

For large files, the tool processes texts sequentially. For better performance with very large datasets, consider:

1. Splitting files into smaller batches
2. Using the Python API with parallel processing
3. Implementing rate limiting for API calls

## Testing

Run the included test suite:

```bash
python test_examples.py
```

This will:
- Test 10 example texts
- Show accuracy metrics
- Save detailed results to `test_results.json`


## Best Practices

1. **Use appropriate models**: GPT-3.5-turbo for cost-effectiveness, GPT-4 for higher accuracy
2. **Batch processing**: Process multiple texts together for efficiency
3. **Error handling**: Always check for `error` field in results
4. **Label consistency**: Use consistent label names across configurations
5. **API key security**: Never commit `.env` file to version control

## Limitations

- Requires internet connection for API calls
- Subject to OpenAI API rate limits
- Costs per API call (though minimal with GPT-3.5-turbo)
- Classification quality depends on prompt design and model choice

## Contributing

To extend this tool:

1. Modify `config.json` for different label sets
2. Customize prompt templates for specific use cases
3. Add new output formats by modifying the `ClassificationResult` class
4. Implement caching for repeated classifications

## License

This project is provided as-is for text classification purposes.

## Support

For issues or questions:

1. **Check API key**: Ensure your OpenAI API key is valid and has credits
2. **Verify Python version**: Requires Python 3.8 or higher
3. **Install dependencies**: Run `pip install -r requirements.txt`
4. **Check API status**: Verify OpenAI API is operational
5. **Review error messages**: The tool provides detailed error information

## Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Pricing](https://openai.com/pricing)
- [Python Documentation](https://docs.python.org/3/)

---



