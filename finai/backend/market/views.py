from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .services.tickers import list_supported_tickers
from .services.indicators import compute_indicators_for_symbol
from .services.classifier import classify_symbol
from .services.yf_client import fetch_history
from .services.db import get_user_preferences, set_user_preferences
from .services.repository import get_portfolio, save_portfolio, list_news, list_chat_sessions, create_chat_session, list_messages, add_message
from .models.portfolio import Portfolio, Holding
from .models.chat import ChatMessage

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
	return Response({'status': 'ok'})

@api_view(['GET'])
def list_tickers(request):
	return Response({'tickers': list_supported_tickers()})

@api_view(['GET'])
def get_indicators(request, symbol: str):
	period = request.query_params.get('period', '1y')
	interval = request.query_params.get('interval', '1d')
	try:
		ind = compute_indicators_for_symbol(symbol, period=period, interval=interval)
		return Response(ind)
	except Exception as exc:
		return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def scan_market(request):
	period = request.query_params.get('period', '1y')
	interval = request.query_params.get('interval', '1d')
	results = {'buy_opportunities': [], 'sell_risks': []}
	for t in list_supported_tickers():
		try:
			data = fetch_history(t['symbol'], period=period, interval=interval)
			ind = compute_indicators_for_symbol(t['symbol'], period=period, interval=interval, source_df=data)
			label, score = classify_symbol(ind)
			row = {'symbol': t['symbol'], 'name': t['name'], 'label': label, 'score': score, 'indicators': ind}
			if label == 'buy':
				results['buy_opportunities'].append(row)
			elif label == 'sell':
				results['sell_risks'].append(row)
		except Exception:
			continue
	return Response(results)

@api_view(['GET'])
def my_preferences(request):
	uid = getattr(request.user, 'uid', None)
	prefs = get_user_preferences(uid) if uid else {}
	return Response({'preferences': prefs})

@api_view(['POST'])
def save_preferences(request):
	uid = getattr(request.user, 'uid', None)
	prefs = request.data.get('preferences', {})
	stored = set_user_preferences(uid, prefs) if uid else {}
	return Response({'preferences': stored})

@api_view(['GET'])
def portfolio_get(request):
	uid = getattr(request.user, 'uid', None)
	pf = get_portfolio(uid)
	return Response({
		'name': pf.name,
		'value': pf.value,
		'returns_abs': pf.returns_abs,
		'returns_pct': pf.returns_pct,
		'holdings': [h.to_dict() for h in pf.holdings]
	})

@api_view(['POST'])
def portfolio_save(request):
	uid = getattr(request.user, 'uid', None)
	payload = request.data or {}
	holdings = [Holding.from_dict(x) for x in payload.get('holdings', [])]
	pf = Portfolio(uid=uid, name=payload.get('name','Principal'), value=float(payload.get('value',0.0)), returns_abs=float(payload.get('returns_abs',0.0)), returns_pct=float(payload.get('returns_pct',0.0)), holdings=holdings)
	save_portfolio(uid, pf)
	return Response({'ok': True})

@api_view(['GET'])
@permission_classes([AllowAny])
def news_list(request):
	items = [n.to_dict() for n in list_news()]
	return Response({'news': items})

@api_view(['GET'])
def chat_sessions(request):
	uid = getattr(request.user, 'uid', None)
	sessions = [ {'title': s.title} for s in list_chat_sessions(uid) ]
	return Response({'sessions': sessions})

@api_view(['POST'])
def chat_create(request):
	uid = getattr(request.user, 'uid', None)
	title = (request.data or {}).get('title', 'Chat con FinAI')
	sid = create_chat_session(uid, title)
	return Response({'session_id': sid})

@api_view(['GET'])
def chat_messages(request):
	uid = getattr(request.user, 'uid', None)
	session_id = request.query_params.get('session_id')
	msgs = [m.to_dict() for m in list_messages(uid, session_id)]
	return Response({'messages': msgs})

@api_view(['POST'])
def chat_add_message(request):
	uid = getattr(request.user, 'uid', None)
	session_id = (request.data or {}).get('session_id')
	role = (request.data or {}).get('role', 'user')
	content = (request.data or {}).get('content', '')
	add_message(uid, session_id, ChatMessage(role=role, content=content))
	return Response({'ok': True})