from config import RECOMMENDATION_THRESHOLDS


def get_recommendation(total_score):
    """
    Get recommendation based on total score
    
    Args:
        total_score: Sum of all indicator scores
    
    Returns:
        String recommendation
    """
    if total_score >= RECOMMENDATION_THRESHOLDS['strong_buy']:
        return "STRONG BUY"
    elif total_score >= RECOMMENDATION_THRESHOLDS['buy']:
        return "BUY"
    elif total_score >= RECOMMENDATION_THRESHOLDS['hold']:
        return "HOLD"
    elif total_score >= RECOMMENDATION_THRESHOLDS['weak_sell']:
        return "WEAK SELL"
    else:
        return "AVOID"


def analyze_multiple_stocks(tickers):
    """
    Analyze multiple stocks and return results
    
    Args:
        tickers: List of stock symbols
    
    Returns:
        List of analysis results
    """
    from analysis.analyzer import analyze_stock
    
    results = []
    for ticker in tickers:
        result = analyze_stock(ticker)
        if result:
            results.append(result)
    
    return results


def print_summary(results):
    """
    Print summary table of multiple analyses
    
    Args:
        results: List of analysis results
    """
    print("\n" + "="*70)
    print("SUMMARY TABLE")
    print("="*70)
    print(f"{'Ticker':<10} {'Price':<12} {'Score':<10} {'%':<8} {'Recommendation':<20}")
    print("-"*70)
    
    for result in results:
        print(f"{result['ticker']:<10} ${result['current_price']:<11.2f} "
              f"{result['total_score']:<9.1f} {result['percentage']:<7.1f}% {result['recommendation']:<20}")
    
    print("="*70 + "\n")