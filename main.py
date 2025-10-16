from analysis.analyzer import analyze_stock
from utils.helpers import analyze_multiple_stocks, print_summary


if __name__ == "__main__":
    # Example 1: Analyze a single stock
    print("Example 1: Single Stock Analysis")
    result = analyze_stock("AAPL")
    
    # Example 2: Analyze multiple stocks
    print("\n\nExample 2: Multiple Stock Analysis")
    tickers = ["MSFT", "GOOGL", "TSLA", "NVDA"]
    results = analyze_multiple_stocks(tickers)
    print_summary(results)