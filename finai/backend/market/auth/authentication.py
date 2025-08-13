from typing import Tuple, Optional
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

from .firebase import verify_id_token

class FirebaseUser:
	def __init__(self, uid: str, email: Optional[str] = None, name: Optional[str] = None):
		self.id = uid
		self.uid = uid
		self.email = email
		self.username = uid
		self.first_name = name or ''
		self.is_authenticated = True


class FirebaseAuthentication(BaseAuthentication):
	keyword = b'Bearer'

	def authenticate(self, request) -> Optional[Tuple[FirebaseUser, None]]:
		# Allow unauthenticated for health endpoint via permission override
		auth = get_authorization_header(request).split()
		if not auth or auth[0].lower() != self.keyword.lower():
			return None
		if len(auth) == 1:
			raise AuthenticationFailed('Cabecera Authorization inválida.')
		token = auth[1].decode('utf-8')
		try:
			payload = verify_id_token(token)
		except Exception as exc:
			raise AuthenticationFailed(f'Token inválido: {exc}')
		return FirebaseUser(uid=payload.get('uid'), email=payload.get('email'), name=payload.get('name')), None

	def authenticate_header(self, request) -> str:
		return 'Bearer'