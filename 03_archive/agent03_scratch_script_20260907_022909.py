import json
import sys
import pandas as pd
import numpy as np

CACHE_PATH = "02_output/raw_cache_20260906.json"

with open(CACHE_PATH) as f:
    cache = json.load(f)

results = cache.get("results", {})


def series_to_df(raw_series):
    rows = []
    for date_str, vals in raw_series.items():
        rows.append({
            "date": pd.to_datetime(date_str),
            "open": float(vals["1. open"]),
            "high": float(vals["2. high"]),
            "low": float(vals["3. low"]),
            "close": float(vals["4. close"]),
            "volume": float(vals["5. volume"]),
        })
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


def rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False, min_periods=fast).mean()
    ema_slow = close.ewm(span=slow, adjust=False, min_periods=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False, min_periods=signal).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


analysis = {}

for ticker, raw in results.items():
    series = raw.get("Time Series (Daily)", {})
    df = series_to_df(series)
    n = len(df)

    out = {"n_days": n}

    if n >= 20:
        sma20 = df["close"].rolling(20).mean().iloc[-1]
        out["sma20"] = round(sma20, 2)
    else:
        out["sma20"] = "insufficient history"

    if n >= 50:
        sma50 = df["close"].rolling(50).mean().iloc[-1]
        out["sma50"] = round(sma50, 2)
    else:
        out["sma50"] = "insufficient history"

    if n >= 15:
        rsi_val = rsi(df["close"], 14).iloc[-1]
        out["rsi14"] = round(rsi_val, 2) if pd.notna(rsi_val) else "insufficient history"
    else:
        out["rsi14"] = "insufficient history"

    if n >= 35:
        macd_line, signal_line, hist = macd(df["close"])
        out["macd"] = round(macd_line.iloc[-1], 3)
        out["macd_signal"] = round(signal_line.iloc[-1], 3)
        out["macd_hist"] = round(hist.iloc[-1], 3)
    else:
        out["macd"] = out["macd_signal"] = out["macd_hist"] = "insufficient history"

    if n >= 20:
        out["support_20d"] = round(df["low"].tail(20).min(), 2)
        out["resistance_20d"] = round(df["high"].tail(20).max(), 2)
    else:
        out["support_20d"] = out["resistance_20d"] = "insufficient history"

    if n >= 20:
        recent_vol = df["volume"].tail(10).mean()
        prior_vol = df["volume"].tail(20).head(10).mean()
        pct_change = (recent_vol - prior_vol) / prior_vol * 100 if prior_vol else None
        out["volume_recent_10d_avg"] = int(recent_vol)
        out["volume_prior_10d_avg"] = int(prior_vol)
        out["volume_trend_pct"] = round(pct_change, 1) if pct_change is not None else "insufficient history"
    else:
        out["volume_trend_pct"] = "insufficient history"

    if n >= 22:
        past_close = df["close"].iloc[-22]
        cur_close = df["close"].iloc[-1]
        momentum_pct = (cur_close - past_close) / past_close * 100
        out["momentum_1m_pct"] = round(momentum_pct, 2)
    else:
        out["momentum_1m_pct"] = "insufficient history"

    out["latest_close"] = round(df["close"].iloc[-1], 2)
    out["latest_date"] = df["date"].iloc[-1].strftime("%Y-%m-%d")

    numeric_ok = all(isinstance(out[k], (int, float)) for k in
                      ["sma20", "sma50", "rsi14", "macd_hist"])
    if numeric_ok:
        close = out["latest_close"]
        bullish = (close > out["sma20"] > out["sma50"]) and (40 <= out["rsi14"] <= 70) and (out["macd_hist"] > 0)
        bearish = (close < out["sma20"] < out["sma50"]) and (out["rsi14"] < 60) and (out["macd_hist"] < 0)
        if bullish:
            view = "Bullish"
        elif bearish:
            view = "Bearish"
        else:
            view = "Neutral"
    else:
        view = "insufficient history"

    out["technical_view"] = view
    analysis[ticker] = out

with open("02_output/.agent03_technical_analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

for t, o in analysis.items():
    print(t, "->", o["technical_view"], "| SMA20:", o["sma20"], "SMA50:", o["sma50"],
          "RSI14:", o["rsi14"], "MACD hist:", o["macd_hist"])
