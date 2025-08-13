from __future__ import annotations
import os
import pandas as pd
import yfinance as yf
from cachetools import TTLCache, cached

# TTL cache: 10 minutes by default, up to 128 symbols/queries
_YF_CACHE = TTLCache(maxsize=128, ttl=int(os.getenv('YF_CACHE_TTL_SECONDS', '600')))


def _cache_key(symbol: str, period: str, interval: str) -> str:
	return f"{symbol}|{period}|{interval}"


@cached(_YF_CACHE, key=lambda symbol, period='1y', interval='1d': _cache_key(symbol, period, interval))
def fetch_history(symbol: str, period: str = '1y', interval: str = '1d') -> pd.DataFrame:
	"""Fetch historical OHLCV data from Yahoo Finance as a DataFrame.
	Columns: Open, High, Low, Close, Adj Close, Volume
	"""
	ticker = yf.Ticker(symbol)
	df = ticker.history(period=period, interval=interval, auto_adjust=False, actions=False)
	if df is None or df.empty:
		raise ValueError(f"No hay datos para {symbol} ({period}/{interval})")
	# Ensure columns are consistent
	for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
		if col not in df.columns:
			raise ValueError(f"Falta columna {col} en datos de {symbol}")
	return df