import pandas as pd
import yfinance as yf
from config import MA_SHORT_PERIOD, MA_LONG_PERIOD, RSI_PERIOD, VOLUME_PERIOD, VIX_TICKER


def calculate_moving_averages(prices, short_period=MA_SHORT_PERIOD, long_period=MA_LONG_PERIOD):
    """
    Calculate short-term and long-term moving averages
    
    Returns:
        Tuple of (short_ma, long_ma)
    """
    short_ma = prices.rolling(window=short_period).mean()
    long_ma = prices.rolling(window=long_period).mean()
    return short_ma, long_ma


def calculate_rsi(prices, period=RSI_PERIOD):
    """
    Calculate Relative Strength Index (RSI)
    
    Returns:
        Series of RSI values (0-100)
    """
    deltas = prices.diff()
    gains = deltas.where(deltas > 0, 0)
    losses = -deltas.where(deltas < 0, 0)
    
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_volume_ratio(volumes, period=VOLUME_PERIOD):
    """
    Calculate how current volume compares to average
    
    Returns:
        Series of volume ratios (current / average)
    """
    avg_volume = volumes.rolling(window=period).mean()
    volume_ratio = volumes / avg_volume
    return volume_ratio


def calculate_vix(ticker=VIX_TICKER):
    """
    Fetch current VIX (market volatility index)
    
    Returns:
        Float value of VIX
    """
    try:
        vix = yf.Ticker(ticker)
        vix_data = vix.history(period="1d")
        current_vix = vix_data['Close'].iloc[-1] if len(vix_data) > 0 else 20
        return current_vix
    except:
        return 20  # Default if error