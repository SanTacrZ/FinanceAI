from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .services.tickers import list_supported_tickers
from .services.indicators import compute_indicators_for_symbol
from .services.classifier import classify_symbol
from .services.yf_client import fetch_history
from .services.db import get_user_preferences, set_user_preferences

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