from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .base import TimestampedModel

ImpactLevel = Literal['LOW', 'MEDIUM', 'HIGH']


@dataclass
class NewsArticle(TimestampedModel):
	category: str = ''
	title: str = ''
	summary: str = ''
	image_url: str = ''
	impact: ImpactLevel = 'LOW'
	source: str = ''