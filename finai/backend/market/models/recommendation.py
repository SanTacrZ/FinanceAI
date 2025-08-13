from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .base import TimestampedModel

RiskLevel = Literal['LOW', 'MEDIUM', 'HIGH']


@dataclass
class Recommendation(TimestampedModel):
	symbol: str = ''
	title: str = ''
	description: str = ''
	risk: RiskLevel = 'LOW'