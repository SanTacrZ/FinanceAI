from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, Any


def utcnow() -> datetime:
	return datetime.now(timezone.utc)


@dataclass
class TimestampedModel:
	created_at: datetime = field(default_factory=utcnow)
	updated_at: datetime = field(default_factory=utcnow)

	def touch(self) -> None:
		self.updated_at = utcnow()

	def to_dict(self) -> Dict[str, Any]:
		data = asdict(self)
		# Convert datetimes to ISO
		for k, v in list(data.items()):
			if isinstance(v, datetime):
				data[k] = v.isoformat()
		return data

	@classmethod
	def from_dict(cls, data: Dict[str, Any]):
		kw = dict(data)
		for key in ['created_at', 'updated_at']:
			val = kw.get(key)
			if isinstance(val, str):
				kw[key] = datetime.fromisoformat(val)
		return cls(**kw)