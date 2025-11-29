"""
Technical Indicators Module

This module calculates technical indicators used in the trading strategy:
- Moving Averages (MA50, MA200): Identify trends
- RSI (Relative Strength Index): Measure momentum
- Volume Ratio: Confirm market interest
- VIX: Assess market volatility
"""

import pandas as pd
import yfinance as yf
from config import MA_SHORT_PERIOD, MA_LONG_PERIOD, RSI_PERIOD, VOLUME_PERIOD, VIX_TICKER


def calculate_moving_averages(prices, short_period=MA_SHORT_PERIOD, long_period=MA_LONG_PERIOD):
    """
    Calculate short-term and long-term moving averages

    Moving averages smooth out price data to identify trends:
    - MA50 (short): Captures recent price momentum
    - MA200 (long): Shows overall trend direction

    When price > both MAs, the stock is in a strong uptrend (bullish signal)

    Args:
        prices: Pandas Series of closing prices
        short_period: Window for short MA (default 50 days)
        long_period: Window for long MA (default 200 days)

    Returns:
        Tuple of (short_ma, long_ma) as Pandas Series
    """
    short_ma = prices.rolling(window=short_period).mean()
    long_ma = prices.rolling(window=long_period).mean()
    return short_ma, long_ma


def calculate_rsi(prices, period=RSI_PERIOD):
    """
    Calculate Relative Strength Index (RSI)

    RSI measures momentum on a scale of 0-100:
    - RSI > 70: Overbought (may reverse down)
    - RSI < 30: Oversold (may reverse up)
    - RSI 40-60: Neutral momentum

    Our strategy prefers RSI in neutral/oversold zones to avoid buying
    at peak prices.

    Args:
        prices: Pandas Series of closing prices
        period: Lookback window (default 14 days)

    Returns:
        Series of RSI values (0-100)
    """
    # Calculate price changes
    deltas = prices.diff()
    gains = deltas.where(deltas > 0, 0)
    losses = -deltas.where(deltas < 0, 0)

    # Calculate average gains and losses
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()

    # Compute RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_volume_ratio(volumes, period=VOLUME_PERIOD):
    """
    Calculate how current volume compares to average

    High volume confirms price movements:
    - Volume > 1.25x average: Strong interest (bullish confirmation)
    - Volume < 0.5x average: Weak interest (avoid trading)

    Volume validates whether a price move is genuine or a false signal.

    Args:
        volumes: Pandas Series of trading volumes
        period: Lookback window for average (default 20 days)

    Returns:
        Series of volume ratios (current / average)
    """
    avg_volume = volumes.rolling(window=period).mean()
    volume_ratio = volumes / avg_volume
    return volume_ratio


def calculate_vix(ticker=VIX_TICKER):
    """
    Fetch current VIX (market volatility index)

    VIX is the "fear gauge" for the stock market:
    - VIX < 18: Low volatility (safe to trade)
    - VIX 18-30: Moderate volatility (caution)
    - VIX > 30: High volatility (avoid new positions)

    High VIX often coincides with market crashes and panic selling.

    Args:
        ticker: VIX ticker symbol (default "^VIX")

    Returns:
        Float value of current VIX
    """
    try:
        vix = yf.Ticker(ticker)
        vix_data = vix.history(period="1d")
        current_vix = vix_data['Close'].iloc[-1] if len(vix_data) > 0 else 20
        return current_vix
    except:
        # Return default moderate value if fetch fails
        return 20