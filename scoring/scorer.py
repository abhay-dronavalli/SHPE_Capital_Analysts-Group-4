import pandas as pd
from config import SCORE_RANGES


def score_peg_ratio(peg):
    """Score PEG Ratio (0-5 points) - Lower is better"""
    if peg is None or peg <= 0:
        return 2  # Give benefit of doubt if missing data
    elif peg <= SCORE_RANGES['peg_ratio'][0]:  # <= 1.5
        return 5
    elif peg <= SCORE_RANGES['peg_ratio'][1]:  # <= 2.5
        return 4
    elif peg <= SCORE_RANGES['peg_ratio'][2]:  # <= 3.5
        return 3
    else:
        return 1


def score_operating_margin(margin):
    """Score Operating Margin (0-5 points) - Higher is better"""
    if margin is None or margin < 0:
        return 1
    elif margin > SCORE_RANGES['operating_margin'][1]:  # > 10%
        return 5
    elif margin > SCORE_RANGES['operating_margin'][0]:  # > 1%
        return 3
    else:
        return 1


def score_free_cash_flow(fcf, revenue):
    """Score Free Cash Flow (0-5 points) - Positive is good"""
    if fcf is None or revenue is None or revenue == 0:
        return 2
    
    fcf_margin = fcf / revenue
    
    if fcf_margin < 0:
        return 1
    elif fcf_margin > SCORE_RANGES['fcf_margin'][1]:  # > 10%
        return 5
    elif fcf_margin > SCORE_RANGES['fcf_margin'][0]:  # > 2%
        return 3
    elif fcf_margin > 0:
        return 2
    else:
        return 1


def score_revenue_growth(growth):
    """Score Revenue Growth YoY (0-5 points) - Higher is better"""
    if growth is None:
        return 2
    elif growth < 0:
        return 1
    elif growth > SCORE_RANGES['revenue_growth'][1]:  # > 10%
        return 5
    elif growth > SCORE_RANGES['revenue_growth'][0]:  # > 3%
        return 3
    elif growth > 0:
        return 2
    else:
        return 1


def score_fcf_growth(growth):
    """Score FCF Growth YoY (0-5 points) - Higher is better"""
    if growth is None:
        return 2
    elif growth < 0:
        return 1
    elif growth > SCORE_RANGES['fcf_growth'][1]:  # > 10%
        return 5
    elif growth > SCORE_RANGES['fcf_growth'][0]:  # > 0%
        return 3
    else:
        return 1


def score_debt_to_equity(de_ratio):
    """Score Debt-to-Equity Ratio (0-5 points) - Lower is better"""
    if de_ratio is None or de_ratio < 0:
        return 2
    elif de_ratio < SCORE_RANGES['debt_to_equity'][0]:  # < 0.5
        return 5
    elif de_ratio < SCORE_RANGES['debt_to_equity'][1]:  # < 1.5
        return 4
    elif de_ratio < SCORE_RANGES['debt_to_equity'][2]:  # < 2.5
        return 3
    else:
        return 1


def score_trend(price, ma50, ma200):
    """Score Trend based on moving averages (0-5 points)"""
    if pd.isna(price) or pd.isna(ma50) or pd.isna(ma200):
        return 2
    
    if price > ma200 and price > ma50:
        return 5  # Strong uptrend
    elif price > ma50 and price > (ma200 * 0.98):  # Close to 200MA
        return 4  # Uptrend
    elif price > ma50:
        return 3  # Recovering
    elif price > ma200:
        return 2  # Mixed
    else:
        return 1  # Downtrend


def score_rsi(rsi):
    """Score RSI for momentum (0-5 points) - 35-55 is ideal"""
    if rsi is None or pd.isna(rsi):
        return 2
    elif rsi < SCORE_RANGES['rsi'][0]:  # < 35 (oversold, building)
        return 4
    elif rsi < SCORE_RANGES['rsi'][1]:  # < 55 (good zone)
        return 5
    elif rsi < SCORE_RANGES['rsi'][2]:  # < 70 (getting hot)
        return 3
    else:  # >= 70 (overbought)
        return 1


def score_volume(volume_ratio):
    """Score Volume (0-5 points) - Above average is good"""
    if volume_ratio is None or pd.isna(volume_ratio):
        return 2
    elif volume_ratio > SCORE_RANGES['volume_ratio'][1]:  # > 1.20
        return 5
    elif volume_ratio > SCORE_RANGES['volume_ratio'][0]:  # > 1.05
        return 3
    elif volume_ratio > 0.8:
        return 2
    else:
        return 1


def score_vix(vix):
    """Score Market Volatility (0-5 points) - Lower is better"""
    if vix is None:
        return 3
    elif vix < SCORE_RANGES['vix'][0]:  # < 20
        return 5
    elif vix < SCORE_RANGES['vix'][1]:  # < 28
        return 4
    elif vix < SCORE_RANGES['vix'][2]:  # < 35
        return 2
    else:  # >= 35
        return 1