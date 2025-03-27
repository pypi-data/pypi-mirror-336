from pydantic import BaseModel
from typing import List, Optional

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