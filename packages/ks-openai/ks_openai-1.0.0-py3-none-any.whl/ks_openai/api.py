import os
from pydantic import BaseModel, Field
from typing import List, Optional
from .utils import make_request


class Message(BaseModel):
    role: str
    content: str

class ContentFilterSeverity(BaseModel):
    filtered: bool
    severity: str

class OpenAIResponseChoiceContentFilterResults(BaseModel):
    hate: ContentFilterSeverity
    self_harm: ContentFilterSeverity
    sexual: ContentFilterSeverity
    violence: ContentFilterSeverity

class OpenAIResponseChoice(BaseModel):
    message: Message
    content_filter_results: Optional[OpenAIResponseChoiceContentFilterResults] = None
    finish_reason: str
    index: int

class OpenAIResponseUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class OpenAIResponse(BaseModel):
    id: str
    choices: List[OpenAIResponseChoice]
    created: int
    model: str
    usage: OpenAIResponseUsage


def generate_response(
    model: str,
    messages: List[dict],
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    frequency_penalty: Optional[float] = None,
    presence_penalty: Optional[float] = None,
    stop: Optional[List[str]] = None
) -> OpenAIResponse:
    """
    Generate a response using the OpenAI API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    url = "http://20.197.22.86:3000/api/model/openai"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Initialize payload with required parameters
    payload = {
        "model": model,
        "messages": messages,
    }
    
    # Add optional parameters only if they are not None
    if temperature is not None:
        payload["temperature"] = temperature
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if top_p is not None:
        payload["top_p"] = top_p
    if frequency_penalty is not None:
        payload["frequency_penalty"] = frequency_penalty
    if presence_penalty is not None:
        payload["presence_penalty"] = presence_penalty
    if stop is not None:
        payload["stop"] = stop

    response_data = make_request("POST", url, headers=headers, json=payload)
    return OpenAIResponse(**response_data)