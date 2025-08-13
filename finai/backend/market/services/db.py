from __future__ import annotations
from typing import Any, Dict
from firebase_admin import firestore
from ..auth.firebase import initialize_firebase_if_needed


def get_db():
	initialize_firebase_if_needed()
	return firestore.client()


def get_user_preferences(uid: str) -> Dict[str, Any]:
	db = get_db()
	doc_ref = db.collection('users').document(uid)
	doc = doc_ref.get()
	if doc.exists:
		data = doc.to_dict() or {}
		return data.get('preferences', {})
	return {}


def set_user_preferences(uid: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
	db = get_db()
	doc_ref = db.collection('users').document(uid)
	doc_ref.set({'preferences': preferences}, merge=True)
	return preferences