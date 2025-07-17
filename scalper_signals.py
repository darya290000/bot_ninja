import requests
from config import API_KEY, API_SECRET

def get_price(symbol):
    url = f"https://api.mexc.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"❌ خطا در دریافت قیمت {symbol}: {e}")
        return None

def ema(prices, period):
    if len(prices) < period:
        return None
    k = 2 / (period + 1)
    ema_val = prices[0]
    for price in prices[1:]:
        ema_val = price * k + ema_val * (1 - k)
    return ema_val

def rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    gains, losses = 0, 0
    for i in range(1, period + 1):
        change = prices[-i] - prices[-i - 1]
        if change > 0:
            gains += change
        else:
            losses -= change
    avg_gain = gains / period
    avg_loss = losses / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def scalper_strategy(symbol, prices):
    if len(prices) < 26:
        return None
    ema_fast = ema(prices, 9)
    ema_slow = ema(prices, 21)
    current_rsi = rsi(prices)
    if ema_fast is None or ema_slow is None or current_rsi is None:
        return None
    if ema_fast > ema_slow and current_rsi < 70:
        return f"🟢 سیگنال خرید: {symbol} | EMA9 > EMA21 | RSI={round(current_rsi,1)}"
    elif ema_fast < ema_slow and current_rsi > 30:
        return f"🔴 سیگنال فروش: {symbol} | EMA9 < EMA21 | RSI={round(current_rsi,1)}"
    return None

def analyze_symbol(symbol, history_dict):
    price = get_price(symbol)
    if not price:
        return None
    history = history_dict.get(symbol, [])
    history.append(price)
    history = history[-50:]
    history_dict[symbol] = history
    return scalper_strategy(symbol, history)
