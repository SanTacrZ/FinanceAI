from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any
from .base import TimestampedModel


class SignalLabel:
	BUY = 'buy'
	SELL = 'sell'
	NEUTRAL = 'neutral'


@dataclass
class Asset(TimestampedModel):
	symbol: str = ''
	name: str = ''
	kind: str = 'stock'  # stock | index | etf
	currency: str = 'COP'
	country: str = 'CO'


@dataclass
class Quote(TimestampedModel):
	symbol: str = ''
	price: float = 0.0
	change_pct: float = 0.0


@dataclass
class IndicatorSnapshot(TimestampedModel):
	symbol: str = ''
	close: float = 0.0
	rsi: float = 0.0
	macd: float = 0.0
	macd_signal: float = 0.0
	macd_hist: float = 0.0
	vwap: float = 0.0
	ema_25: float = 0.0
	ema_50: float = 0.0
	ema_100: float = 0.0
	ema_200: float = 0.0
	ema_1000: float = 0.0
	signal: str = SignalLabel.NEUTRAL
	score: float = 0.0

	def to_firestore(self) -> Dict[str, Any]:
		return self.to_dict()