from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Literal
from .base import TimestampedModel

MessageRole = Literal['user', 'assistant', 'system']


@dataclass
class ChatMessage(TimestampedModel):
	role: MessageRole = 'user'
	content: str = ''


@dataclass
class ChatSession(TimestampedModel):
	uid: str = ''
	title: str = 'Chat con FinAI'
	messages: List[ChatMessage] = field(default_factory=list)