from __future__ import annotations
from typing import List, Dict, Any
from uuid import uuid4
from firebase_admin import firestore
from .db import get_db
from ..models.portfolio import Portfolio, Holding
from ..models.chat import ChatSession, ChatMessage
from ..models.news import NewsArticle


def _users():
	return get_db().collection('users')


# Portfolio

def get_portfolio(uid: str) -> Portfolio:
	doc = _users().document(uid).collection('portfolios').document('default').get()
	if doc.exists:
		data = doc.to_dict() or {}
		holdings = [Holding.from_dict(x) for x in data.get('holdings', [])]
		return Portfolio(uid=uid, name=data.get('name','Principal'), holdings=holdings, value=float(data.get('value',0.0)), returns_abs=float(data.get('returns_abs',0.0)), returns_pct=float(data.get('returns_pct',0.0)))
	return Portfolio(uid=uid)


def save_portfolio(uid: str, portfolio: Portfolio) -> Portfolio:
	_ = _users().document(uid).collection('portfolios').document('default').set({
		'name': portfolio.name,
		'value': portfolio.value,
		'returns_abs': portfolio.returns_abs,
		'returns_pct': portfolio.returns_pct,
		'holdings': [h.to_dict() for h in portfolio.holdings],
	}, merge=True)
	return portfolio


# Chat

def list_chat_sessions(uid: str) -> List[ChatSession]:
	ref = _users().document(uid).collection('chats')
	docs = ref.stream()
	sessions: List[ChatSession] = []
	for d in docs:
		data = d.to_dict() or {}
		sessions.append(ChatSession(uid=uid, title=data.get('title','Chat con FinAI')))
	return sessions


def create_chat_session(uid: str, title: str = 'Chat con FinAI') -> str:
	sid = uuid4().hex[:12]
	_users().document(uid).collection('chats').document(sid).set({'title': title})
	return sid


def list_messages(uid: str, session_id: str) -> List[ChatMessage]:
	ref = _users().document(uid).collection('chats').document(session_id).collection('messages').order_by('created_at')
	docs = ref.stream()
	res: List[ChatMessage] = []
	for d in docs:
		v = d.to_dict() or {}
		res.append(ChatMessage(role=v.get('role','assistant'), content=v.get('content','')))
	return res


def add_message(uid: str, session_id: str, msg: ChatMessage) -> None:
	_ = _users().document(uid).collection('chats').document(session_id).collection('messages').add({
		'role': msg.role,
		'content': msg.content,
		'created_at': firestore.SERVER_TIMESTAMP,
	})


# News (demo static)

def list_news() -> List[NewsArticle]:
	return [
		NewsArticle(category='ECONOMY', title='Colombian Peso Strengthens Against the Dollar', summary='El peso se fortalece por precios del petróleo y flujos de inversión.', image_url='', impact='HIGH', source='Internal'),
		NewsArticle(category='FINANCE', title='Central Bank Holds Steady on Rates', summary='El BanRep mantiene tasas para contener inflación.', image_url='', impact='MEDIUM', source='Internal'),
	]