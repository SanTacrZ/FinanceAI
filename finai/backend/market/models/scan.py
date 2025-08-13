from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .base import TimestampedModel
from .asset import IndicatorSnapshot


@dataclass
class ScreenerSignal(TimestampedModel):
	symbol: str = ''
	name: str = ''
	label: str = 'neutral'  # buy | sell | neutral
	score: float = 0.0
	indicators: IndicatorSnapshot = field(default_factory=IndicatorSnapshot)


@dataclass
class ScanResult(TimestampedModel):
	buy_opportunities: List[ScreenerSignal] = field(default_factory=list)
	sell_risks: List[ScreenerSignal] = field(default_factory=list)
	universe_size: int = 0