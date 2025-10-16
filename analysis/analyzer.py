from data.data_fetcher import fetch_stock_data, fetch_fundamentals
from indicators.technical import calculate_moving_averages, calculate_rsi, calculate_volume_ratio, calculate_vix
from indicators.fundamental import calculate_revenue_growth, calculate_fcf_growth
from scoring.scorer import (
    score_peg_ratio, score_operating_margin, score_free_cash_flow,
    score_revenue_growth, score_fcf_growth, score_debt_to_equity,
    score_trend, score_rsi, score_volume, score_vix
)
from utils.helpers import get_recommendation


def analyze_stock(ticker):
    """
    Complete analysis of a stock
    
    Returns:
        Dictionary with scores and recommendation
    """
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {ticker}")
    print(f"{'='*60}\n")
    
    # Fetch data
    price_data = fetch_stock_data(ticker)
    fundamentals = fetch_fundamentals(ticker)
    
    if price_data.empty:
        print(f"Error: Could not fetch data for {ticker}")
        return None
    
    # Get latest values
    current_price = price_data['Close'].iloc[-1]
    
    # Calculate technical indicators
    ma50, ma200 = calculate_moving_averages(price_data['Close'])
    rsi = calculate_rsi(price_data['Close'])
    volume_ratio = calculate_volume_ratio(price_data['Volume'])
    vix = calculate_vix()
    
    # Get latest technical values
    latest_ma50 = ma50.iloc[-1]
    latest_ma200 = ma200.iloc[-1]
    latest_rsi = rsi.iloc[-1]
    latest_volume_ratio = volume_ratio.iloc[-1]
    
    # Calculate growth metrics
    revenue_growth = calculate_revenue_growth(ticker)
    fcf_growth = calculate_fcf_growth(ticker)
    
    # Calculate scores for all 10 indicators
    scores = {
        '1. PEG Ratio': score_peg_ratio(fundamentals.get('peg_ratio', 0)),
        '2. Operating Margin': score_operating_margin(fundamentals.get('operating_margin', 0)),
        '3. Free Cash Flow': score_free_cash_flow(
            fundamentals.get('free_cash_flow', 0),
            fundamentals.get('revenue', 0)
        ),
        '4. Revenue Growth': score_revenue_growth(revenue_growth),
        '5. FCF Growth': score_fcf_growth(fcf_growth),
        '6. Debt-to-Equity': score_debt_to_equity(fundamentals.get('debt_to_equity', 0)),
        '7. Trend (MA50/200)': score_trend(current_price, latest_ma50, latest_ma200),
        '8. Momentum (RSI)': score_rsi(latest_rsi),
        '9. Volume': score_volume(latest_volume_ratio),
        '10. VIX Filter': score_vix(vix),
    }
    
    # Calculate total score
    total_score = sum(scores.values())
    percentage = (total_score / 50) * 100
    recommendation = get_recommendation(total_score)
    
    # Print results
    print(f"Current Price: ${current_price:.2f}")
    print(f"50-day MA: ${latest_ma50:.2f}")
    print(f"200-day MA: ${latest_ma200:.2f}")
    print(f"RSI: {latest_rsi:.2f}")
    print(f"Volume Ratio: {latest_volume_ratio:.2f}x")
    print(f"VIX: {vix:.2f}\n")
    
    print("INDICATOR SCORES (0-5 each):")
    print("-" * 40)
    for indicator, score in scores.items():
        print(f"{indicator:.<35} {score:>4.1f}")
    
    print("-" * 40)
    print(f"{'TOTAL SCORE':.<35} {total_score:>4.1f}/50")
    print(f"{'PERCENTAGE':.<35} {percentage:>4.1f}%")
    print(f"\nRECOMMENDATION: {recommendation}")
    print(f"{'='*60}\n")
    
    return {
        'ticker': ticker,
        'current_price': current_price,
        'scores': scores,
        'total_score': total_score,
        'percentage': percentage,
        'recommendation': recommendation,
    }