# Configuration constants for the trading algorithm

# Technical Indicator Periods
MA_SHORT_PERIOD = 50
MA_LONG_PERIOD = 200
RSI_PERIOD = 14
VOLUME_PERIOD = 20

# Data Fetching
DEFAULT_PERIOD = "5y"
VIX_TICKER = "^VIX"

# Scoring Thresholds - ADJUSTED FOR REALISM
# These are more lenient to allow for actual trading opportunities
SCORE_RANGES = {
    # Valuation: allow stocks up to 3.0 PEG to get 5 points
    'peg_ratio': [1.5, 2.5, 3.5],
    
    # Profitability: lower bar for operating margin
    'operating_margin': [0.01, 0.10],  # 1% to 10%
    
    # FCF: just needs to be positive and reasonable
    'fcf_margin': [0.02, 0.10],  # 2% to 10%
    
    # Growth: 3% growth is acceptable
    'revenue_growth': [3, 10],  # 3% to 10%
    
    # FCF Growth: 0% is acceptable (positive FCF)
    'fcf_growth': [0, 10],  # 0% to 10%
    
    # Debt: up to 2.0 is acceptable
    'debt_to_equity': [0.5, 1.5, 2.5],
    
    # RSI: more forgiving range
    'rsi': [35, 55, 70],
    
    # Volume: lower threshold
    'volume_ratio': [1.05, 1.20],
    
    # VIX: only avoid when very high
    'vix': [20, 28, 35],
}

# Recommendation Thresholds
RECOMMENDATION_THRESHOLDS = {
    'strong_buy': 38,      # Down from 40
    'buy': 28,             # Down from 30
    'hold': 18,            # Down from 20
    'weak_sell': 8,        # Down from 10
    'avoid': 0,
}