import numpy as np
import pandas as pd


def calculate_returns(trades):
    """
    Calculate total return from list of trades
    
    Args:
        trades: List of dicts with trade information
    
    Returns:
        (total_profit, win_rate, num_trades)
    """
    if not trades:
        return 0, 0, 0
    
    total_profit = sum(t['profit'] for t in trades)
    winning_trades = sum(1 for t in trades if t['profit'] > 0)
    win_rate = (winning_trades / len(trades)) * 100
    
    return total_profit, win_rate, len(trades)


def calculate_max_drawdown(equity_curve):
    """
    Calculate maximum drawdown from equity curve
    
    Args:
        equity_curve: List of dicts with 'equity' values
    
    Returns:
        Max drawdown as percentage
    """
    if len(equity_curve) < 2:
        return 0
    
    equity_values = [e['equity'] for e in equity_curve]
    
    peak = equity_values[0]
    max_drawdown = 0
    
    for value in equity_values:
        if value > peak:
            peak = value
        
        drawdown = (peak - value) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    return max_drawdown * 100


def calculate_cagr(start_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate
    
    Args:
        start_value: Initial investment
        end_value: Final account value
        years: Number of years
    
    Returns:
        CAGR as percentage
    """
    if start_value == 0 or years == 0:
        return 0
    
    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
    return cagr


def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratio (risk-adjusted return)
    
    Args:
        returns: List of period returns
        risk_free_rate: Annual risk-free rate (default 2%)
    
    Returns:
        Sharpe ratio
    """
    if len(returns) < 2:
        return 0
    
    returns_array = np.array(returns)
    excess_returns = returns_array - (risk_free_rate / 252)  # Daily risk-free rate
    
    if np.std(excess_returns) == 0:
        return 0
    
    sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    return sharpe


def print_trade_summary(trades):
    """
    Print a summary of all trades
    
    Args:
        trades: List of trade dictionaries
    """
    if not trades:
        print("No trades to display")
        return
    
    print("\nTRADE SUMMARY")
    print("="*90)
    print(f"{'#':<4} {'Entry Date':<12} {'Entry $':<10} {'Exit Date':<12} {'Exit $':<10} {'Profit $':<12} {'Return %':<10}")
    print("-"*90)
    
    for i, trade in enumerate(trades, 1):
        print(f"{i:<4} "
              f"{trade['entry_date'].date()!s:<12} "
              f"${trade['entry_price']:<9.2f} "
              f"{trade['exit_date'].date()!s:<12} "
              f"${trade['exit_price']:<9.2f} "
              f"${trade['profit']:<11.2f} "
              f"{trade['profit_pct']:<9.2f}%")
    
    print("="*90)


def compare_to_buy_and_hold(strategy_return, ticker_return):
    """
    Compare strategy performance to buy-and-hold
    
    Args:
        strategy_return: Return from the trading strategy
        ticker_return: Return from buying and holding
    
    Returns:
        Outperformance percentage
    """
    outperformance = strategy_return - ticker_return
    return outperformance