from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Optional

from .yf_client import fetch_history


def compute_ema(series: pd.Series, span: int) -> pd.Series:
	return series.ewm(span=span, adjust=False).mean()


def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
	change = series.diff()
	gain = np.where(change > 0, change, 0.0)
	loss = np.where(change < 0, -change, 0.0)
	avg_gain = pd.Series(gain, index=series.index).rolling(window=window, min_periods=window).mean()
	avg_loss = pd.Series(loss, index=series.index).rolling(window=window, min_periods=window).mean()
	rs = avg_gain / (avg_loss.replace(0, np.nan))
	rsi = 100 - (100 / (1 + rs))
	return rsi.fillna(method='bfill')


def compute_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
	ema_fast = compute_ema(series, fast)
	ema_slow = compute_ema(series, slow)
	macd_line = ema_fast - ema_slow
	signal_line = macd_line.ewm(span=signal, adjust=False).mean()
	hist = macd_line - signal_line
	return pd.DataFrame({'macd': macd_line, 'signal': signal_line, 'hist': hist})


def compute_vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
	typical_price = (high + low + close) / 3.0
	cum_pv = (typical_price * volume).cumsum()
	cum_vol = volume.cumsum().replace(0, np.nan)
	return cum_pv / cum_vol


EMA_WINDOWS = [25, 50, 100, 200, 1000]


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
	ind = pd.DataFrame(index=df.index)
	ind['close'] = df['Close']
	for w in EMA_WINDOWS:
		ind[f'ema_{w}'] = compute_ema(ind['close'], w)
	ind['rsi_14'] = compute_rsi(ind['close'], 14)
	macd = compute_macd(ind['close'])
	ind = ind.join(macd)
	ind['vwap'] = compute_vwap(df['High'], df['Low'], df['Close'], df['Volume'])
	return ind


def summarize_latest(ind: pd.DataFrame) -> Dict:
	last = ind.dropna().iloc[-1]
	out = {
		'close': float(last['close']),
		'rsi': float(last['rsi_14']),
		'macd': float(last['macd']),
		'macd_signal': float(last['signal']),
		'macd_hist': float(last['hist']),
		'vwap': float(last['vwap']),
	}
	for w in EMA_WINDOWS:
		out[f'ema_{w}'] = float(last[f'ema_{w}'])
	return out


def compute_indicators_for_symbol(symbol: str, period: str = '1y', interval: str = '1d', source_df: Optional[pd.DataFrame] = None) -> Dict:
	df = source_df if source_df is not None else fetch_history(symbol, period=period, interval=interval)
	ind = compute_indicators(df)
	return summarize_latest(ind)