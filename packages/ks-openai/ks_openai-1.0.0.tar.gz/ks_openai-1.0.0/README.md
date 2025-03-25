# ks_openai

A Python package for interacting with the KS OpenAI-like API.

## Installation

```bash
pip install ks_openai
```

## Configuration

Set your API key as an environment variable:

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

## Basic Usage

```python
from ks_openai import generate_response

# Create a list of messages
messages = [
    {"role": "user", "content": "What is Python?"}
]

# Generate a response
response = generate_response(
    model="gpt-4o-2024-05-13",
    messages=messages
)

# Print the response
print(response.choices[0].message.content)
```

## Advanced Usage

```python
from ks_openai import generate_response

# Example with all parameters
response = generate_response(
    model="gpt-4o-2024-05-13",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"}
    ],
    temperature=0.7,           # Controls randomness (0.0 to 1.0)
    max_tokens=150,           # Maximum length of response
    top_p=0.9,               # Nucleus sampling parameter
    frequency_penalty=0.5,    # Reduces repetition of similar words
    presence_penalty=0.5,     # Encourages new topics
    stop=["\n", "END"]       # Stop sequences
)
```

## API Reference

### `generate_response()`

Main function to generate responses from the API.

#### Parameters:

- `model` (str, required): The model identifier (e.g., "gpt-4o-2024-05-13")
- `messages` (List[dict], required): List of message objects with 'role' and 'content'
- `temperature` (float, optional): Sampling temperature (0.0 to 1.0)
- `max_tokens` (int, optional): Maximum number of tokens in response
- `top_p` (float, optional): Nucleus sampling parameter (0.0 to 1.0)
- `frequency_penalty` (float, optional): Penalty for frequent tokens (0.0 to 2.0)
- `presence_penalty` (float, optional): Penalty for new tokens (0.0 to 2.0)
- `stop` (List[str], optional): List of stopping sequences

#### Returns:

`OpenAIResponse` object with the following structure:
```python
class OpenAIResponse:
    id: str                   # Response identifier
    choices: List[Choice]     # List of response choices
    created: int             # Timestamp
    model: str               # Model used
    usage: Usage             # Token usage statistics
```

## Response Structure

### Message
```python
class Message:
    role: str        # Role of the message (e.g., "user", "assistant")
    content: str     # Content of the message
```

### Content Filter Results
```python
class ContentFilterSeverity:
    filtered: bool   # Whether content was filtered
    severity: str    # Severity level of content

class ContentFilterResults:
    hate: ContentFilterSeverity
    self_harm: ContentFilterSeverity
    sexual: ContentFilterSeverity
    violence: ContentFilterSeverity
```

## Error Handling

```python
try:
    response = generate_response(
        model="gpt-4o-2024-05-13",
        messages=[{"role": "user", "content": "Hello"}]
    )
except Exception as e:
    print(f"Error: {str(e)}")
```

## Examples

### Simple Question-Answer
```python
messages = [{"role": "user", "content": "What is Python?"}]
response = generate_response(model="gpt-4o-2024-05-13", messages=messages)
print(response.choices[0].message.content)
```

### Conversation with Context
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What can I build with it?"}
]
response = generate_response(model="gpt-4o-2024-05-13", messages=messages)
print(response.choices[0].message.content)
```

## Requirements

- Python 3.7+
- requests
- pydantic

## License

This project is licensed under the MIT License.