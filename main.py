"""
Main entry point for the algorithmic trading system

This module demonstrates how to use the trading algorithm for:
1. Single stock analysis
2. Multiple stock comparison
3. Backtesting a trading strategy
"""

from analysis.analyzer import analyze_stock
from utils.helpers import analyze_multiple_stocks, print_summary
from backtest.backtester import Backtester
from backtest.visualizations import create_performance_summary


if __name__ == "__main__":
    print("="*70)
    print("ALGORITHMIC TRADING SYSTEM - SHPE Capital Analysts")
    print("="*70)

    # ========================================================================
    # Example 1: Analyze a Single Stock
    # ========================================================================
    # This performs fundamental + technical analysis on a single stock
    # and provides a BUY/HOLD/SELL recommendation

    # print("\n\nExample 1: Single Stock Analysis")
    # result = analyze_stock("AAPL")

    # ========================================================================
    # Example 2: Analyze Multiple Stocks
    # ========================================================================
    # Compare multiple stocks side-by-side to find the best opportunity

    # print("\n\nExample 2: Multiple Stock Analysis")
    # tickers = ["MSFT", "GOOGL", "TSLA", "NVDA"]
    # results = analyze_multiple_stocks(tickers)
    # print_summary(results)

    # ========================================================================
    # Example 3: Backtest Trading Strategy
    # ========================================================================
    # Test the algorithm on historical data to evaluate performance

    print("\n\nExample 3: Backtesting")

    # Initialize backtester with risk management parameters
    backtester = Backtester(
        ticker="WMT",              # Stock to test
        start_date="2020-01-01",   # Backtest start
        end_date="2024-01-01",     # Backtest end
        initial_capital=10000,     # Starting capital ($10,000)
        stop_loss_pct=0.07,        # 7% stop-loss
        max_position_pct=1.0,      # 100% max position size
        daily_loss_limit_pct=0.10  # 10% daily loss circuit breaker
    )

    # Run the backtest
    results = backtester.run()

    # Generate performance charts
    if results:
        print("\n" + "="*70)
        print("GENERATING PERFORMANCE CHARTS")
        print("="*70)
        create_performance_summary(results, save_dir='charts')
        print("\nCharts saved to 'charts/' directory")
        print("These charts are ready for your presentation!")

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)