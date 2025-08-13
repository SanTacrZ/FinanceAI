from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .base import TimestampedModel


@dataclass
class UserPreferences(TimestampedModel):
	language: str = 'es'
	theme: str = 'light'
	watch_sectors: List[str] = field(default_factory=list)
	notification_email: bool = True
	notification_push: bool = False
	def to_dict(self) -> Dict[str, Any]:
		return super().to_dict()


@dataclass
class RecentlyViewedItem(TimestampedModel):
	symbol: str = ''
	name: str = ''
	category: str = 'stock'  # stock | index | etf


@dataclass
class Watchlist(TimestampedModel):
	name: str = 'Mi lista'
	symbols: List[str] = field(default_factory=list)


@dataclass
class UserProfile(TimestampedModel):
	uid: str = ''
	email: str = ''
	name: str = ''
	photo_url: str = ''
	preferences: UserPreferences = field(default_factory=UserPreferences)
	watchlists: List[Watchlist] = field(default_factory=list)
	recently_viewed: List[RecentlyViewedItem] = field(default_factory=list)

	@classmethod
	def from_firestore(cls, uid: str, data: Dict[str, Any]):
		prefs = UserPreferences.from_dict(data.get('preferences', {})) if data.get('preferences') else UserPreferences()
		wls = [Watchlist.from_dict(x) for x in data.get('watchlists', [])]
		rv = [RecentlyViewedItem.from_dict(x) for x in data.get('recently_viewed', [])]
		return cls(uid=uid, email=data.get('email',''), name=data.get('name',''), photo_url=data.get('photo_url',''), preferences=prefs, watchlists=wls, recently_viewed=rv)

	def to_firestore(self) -> Dict[str, Any]:
		return {
			'email': self.email,
			'name': self.name,
			'photo_url': self.photo_url,
			'preferences': self.preferences.to_dict(),
			'watchlists': [w.to_dict() for w in self.watchlists],
			'recently_viewed': [r.to_dict() for r in self.recently_viewed],
		}