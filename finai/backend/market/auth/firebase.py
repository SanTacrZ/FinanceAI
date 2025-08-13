import os
import json
import firebase_admin
from firebase_admin import credentials, auth

_app = None

def initialize_firebase_if_needed():
	global _app
	if _app is not None:
		return _app
	cred = None
	inline_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
	path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
	if inline_json:
		cred = credentials.Certificate(json.loads(inline_json))
	elif path and os.path.exists(path):
		cred = credentials.Certificate(path)
	else:
		raise RuntimeError('Credenciales de Firebase no configuradas: establece GOOGLE_APPLICATION_CREDENTIALS o FIREBASE_CREDENTIALS_JSON')
	_app = firebase_admin.initialize_app(cred)
	return _app


def verify_id_token(id_token: str) -> dict:
	initialize_firebase_if_needed()
	return auth.verify_id_token(id_token)