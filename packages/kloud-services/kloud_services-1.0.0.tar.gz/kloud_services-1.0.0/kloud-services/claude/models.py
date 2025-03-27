from pydantic import BaseModel
from typing import List, Optional, Any

class Message(BaseModel):
    role: str
    content: str

class ContentBlock(BaseModel):
    type: str
    text: str

class ClaudeResponseContent(BaseModel):
    type: str
    text: str

class ClaudeResponseUsage(BaseModel):
    input_tokens: int
    output_tokens: int

class ClaudeResponse(BaseModel):
    id: str
    type: str
    role: str
    model: str
    content: List[ContentBlock]
    stop_reason: str
    stop_sequence: Optional[str]
    usage: ClaudeResponseUsage