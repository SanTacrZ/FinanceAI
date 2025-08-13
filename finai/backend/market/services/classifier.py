from __future__ import annotations
from typing import Dict, Tuple

THRESHOLDS = {
	'rsi_buy_min': 50,
	'rsi_buy_max': 65,
	'rsi_sell_max': 45,
}


def _score_between(value: float, low: float, high: float) -> float:
	if value < low:
		return 0.0
	if value > high:
		return 0.0
	mid = (low + high) / 2
	return 1.0 - abs(value - mid) / (high - low)


def classify_symbol(ind: Dict) -> Tuple[str, float]:
	close = ind['close']
	rsi = ind['rsi']
	vwap = ind['vwap']
	ema50 = ind['ema_50']
	ema200 = ind['ema_200']
	macd_hist = ind['macd_hist']
	macd = ind['macd']
	signal = ind['macd_signal']

	buy_score = 0.0
	buy_score += 0.3 if close > ema50 and close > ema200 else 0
	buy_score += 0.2 if close > vwap else 0
	buy_score += 0.3 * _score_between(rsi, THRESHOLDS['rsi_buy_min'], THRESHOLDS['rsi_buy_max'])
	buy_score += 0.2 if macd_hist > 0 and macd > signal else 0

	sell_score = 0.0
	sell_score += 0.3 if close < ema50 and close < ema200 else 0
	sell_score += 0.2 if close < vwap else 0
	sell_score += 0.3 if rsi < THRESHOLDS['rsi_sell_max'] else 0
	sell_score += 0.2 if macd_hist < 0 and macd < signal else 0

	if buy_score >= max(0.6, sell_score + 0.15):
		return 'buy', round(buy_score, 3)
	if sell_score >= max(0.6, buy_score + 0.15):
		return 'sell', round(sell_score, 3)
	return 'neutral', round(max(buy_score, sell_score), 3)