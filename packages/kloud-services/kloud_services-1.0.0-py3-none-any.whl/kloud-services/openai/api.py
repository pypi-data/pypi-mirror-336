import os
from pydantic import BaseModel, Field
from typing import List, Optional
from .utils import make_request


class Message(BaseModel):
    role: str
    content: str
import os
from typing import Optional, List, Dict, Any
from .models import OpenAIResponse

class OpenAI:
    def __init__(
        self, 
        api_key: Optional[str] = None,
        base_url: str = "http://20.197.22.86:3000"
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in OPENAI_API_KEY environment variable")
        self.base_url = base_url
        self.chat = Chat(self)

class Chat:
    def __init__(self, client: OpenAI):
        self.client = client
        self.completions = Completions(client)

class Completions:
    def __init__(self, client: OpenAI):
        self.client = client

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[List[str]] = None,
    ) -> OpenAIResponse:
        from .utils import make_request

        url = f"{self.client.base_url}/api/model/openai"
        headers = {
            "Authorization": f"Bearer {self.client.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
        }
        
        for key, value in {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stop": stop
        }.items():
            if value is not None:
                payload[key] = value

        response_data = make_request("POST", url, headers=headers, json=payload)
        return OpenAIResponse(**response_data)
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