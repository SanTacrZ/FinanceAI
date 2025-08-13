from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .base import TimestampedModel


@dataclass
class RankEntry(TimestampedModel):
	symbol: str = ''
	company: str = ''
	price: float = 0.0
	change_pct: float = 0.0


@dataclass
class TopList(TimestampedModel):
	title: str = 'Top Performing Stocks'
	entries: List[RankEntry] = field(default_factory=list)