import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="5y"):
    """
    Fetch historical price data from yfinance
    
    Args:
        ticker: Stock symbol (e.g., "AAPL")
        period: How far back ("1y", "5y", etc.)
    
    Returns:
        DataFrame with OHLCV data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()


def fetch_fundamentals(ticker):
    """
    Fetch fundamental financial data from yfinance
    
    Args:
        ticker: Stock symbol
    
    Returns:
        Dictionary with key financial metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamentals = {
            'ticker': ticker,
            'current_price': info.get('currentPrice', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'peg_ratio': info.get('pegRatio', 0),
            'earnings_per_share': info.get('trailingEps', 0),
            'revenue': info.get('totalRevenue', 0),
            'operating_margin': info.get('operatingMargins', 0),
            'free_cash_flow': info.get('freeCashflow', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'current_ratio': info.get('currentRatio', 0),
        }
        
        return fundamentals
    except Exception as e:
        print(f"Error fetching fundamentals for {ticker}: {e}")
        return {}


def fetch_quarterly_financials(ticker):
    """
    Fetch quarterly financial data
    
    Args:
        ticker: Stock symbol
    
    Returns:
        Tuple of (quarterly_financials, cash_flow)
    """
    try:
        stock = yf.Ticker(ticker)
        quarterly_financials = stock.quarterly_financials
        quarterly_cashflow = stock.quarterly_cashflow
        
        return quarterly_financials, quarterly_cashflow
    except Exception as e:
        print(f"Error fetching quarterly data for {ticker}: {e}")
        return pd.DataFrame(), pd.DataFrame()