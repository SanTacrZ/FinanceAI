from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .base import TimestampedModel


@dataclass
class Holding(TimestampedModel):
	symbol: str = ''
	quantity: float = 0.0
	avg_price: float = 0.0


@dataclass
class PerformancePoint(TimestampedModel):
	date: str = ''
	value: float = 0.0


@dataclass
class Portfolio(TimestampedModel):
	uid: str = ''
	name: str = 'Principal'
	holdings: List[Holding] = field(default_factory=list)
	value: float = 0.0
	returns_abs: float = 0.0
	returns_pct: float = 0.0
	performance: List[PerformancePoint] = field(default_factory=list)