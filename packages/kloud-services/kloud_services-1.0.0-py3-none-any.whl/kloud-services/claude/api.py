import os
from typing import List, Optional, Dict, Any
from .models import ClaudeResponse, Message
from .utils import make_request

class Claude:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "http://20.197.22.86:3000"
    ):
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in CLAUDE_API_KEY environment variable")
        self.base_url = base_url
        self.messages = Messages(self)

class Messages:
    def __init__(self, client: Claude):
        self.client = client

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
    ) -> ClaudeResponse:
        url = f"{self.client.base_url}/api/model/claude"
        headers = {
            "Authorization": f"Bearer {self.client.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": messages,
            "model": model,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p

        response_data = make_request("POST", url, headers=headers, json=payload)
        return ClaudeResponse(**response_data)