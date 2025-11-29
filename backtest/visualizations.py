"""
Visualization module for backtesting results
Generates charts for equity curve, drawdown, and trade distribution
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime


def plot_equity_curve(equity_curve, ticker, save_path=None):
    """
    Plot the equity curve over time

    Args:
        equity_curve: List of dicts with 'date' and 'equity' keys
        ticker: Stock ticker symbol
        save_path: Optional path to save the figure
    """
    # Extract data
    dates = [e['date'] for e in equity_curve]
    equity_values = [e['equity'] for e in equity_curve]

    # Create figure
    plt.figure(figsize=(12, 6))
    plt.plot(dates, equity_values, linewidth=2, color='#2E86AB', label='Portfolio Value')

    # Add horizontal line for initial capital
    initial_capital = equity_values[0]
    plt.axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.7, label='Initial Capital')

    # Formatting
    plt.title(f'Equity Curve - {ticker}', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Equity curve saved to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_drawdown(equity_curve, ticker, save_path=None):
    """
    Plot the drawdown over time

    Args:
        equity_curve: List of dicts with 'date' and 'equity' keys
        ticker: Stock ticker symbol
        save_path: Optional path to save the figure
    """
    # Extract data
    dates = [e['date'] for e in equity_curve]
    equity_values = [e['equity'] for e in equity_curve]

    # Calculate drawdown
    peak = equity_values[0]
    drawdowns = []

    for value in equity_values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak * 100
        drawdowns.append(drawdown)

    # Create figure
    plt.figure(figsize=(12, 6))
    plt.fill_between(dates, drawdowns, 0, color='#A23B72', alpha=0.6)
    plt.plot(dates, drawdowns, linewidth=2, color='#A23B72')

    # Formatting
    plt.title(f'Drawdown Analysis - {ticker}', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Drawdown (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.gca().invert_yaxis()  # Invert so drawdowns go down
    plt.tight_layout()

    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Drawdown chart saved to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_trade_distribution(trades, ticker, save_path=None):
    """
    Plot the distribution of trade returns

    Args:
        trades: List of trade dictionaries
        ticker: Stock ticker symbol
        save_path: Optional path to save the figure
    """
    if not trades:
        print("No trades to plot")
        return

    # Extract profit percentages
    profit_pcts = [t['profit_pct'] for t in trades]

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Subplot 1: Histogram
    ax1.hist(profit_pcts, bins=20, color='#F18F01', alpha=0.7, edgecolor='black')
    ax1.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Break-even')
    ax1.set_title('Distribution of Trade Returns', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Return (%)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Trade sequence
    trade_numbers = list(range(1, len(trades) + 1))
    colors = ['green' if p > 0 else 'red' for p in profit_pcts]
    ax2.bar(trade_numbers, profit_pcts, color=colors, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_title('Trade-by-Trade Returns', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Trade Number', fontsize=12)
    ax2.set_ylabel('Return (%)', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.suptitle(f'{ticker} - Trade Analysis', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Trade distribution saved to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_monthly_returns(equity_curve, ticker, save_path=None):
    """
    Plot monthly returns heatmap

    Args:
        equity_curve: List of dicts with 'date' and 'equity' keys
        ticker: Stock ticker symbol
        save_path: Optional path to save the figure
    """
    # Convert to DataFrame
    df = pd.DataFrame(equity_curve)
    df.set_index('date', inplace=True)

    # Calculate monthly returns
    monthly_equity = df['equity'].resample('ME').last()
    monthly_returns = monthly_equity.pct_change() * 100

    if len(monthly_returns) < 2:
        print("Not enough data for monthly returns")
        return

    # Create pivot table for heatmap
    monthly_returns_df = monthly_returns.to_frame()
    monthly_returns_df['Year'] = monthly_returns_df.index.year
    monthly_returns_df['Month'] = monthly_returns_df.index.month

    pivot_table = monthly_returns_df.pivot_table(
        values='equity',
        index='Year',
        columns='Month',
        aggfunc='mean'
    )

    # Create figure
    plt.figure(figsize=(12, 6))
    im = plt.imshow(pivot_table.values, cmap='RdYlGn', aspect='auto', vmin=-10, vmax=10)

    # Set ticks
    plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.yticks(range(len(pivot_table.index)), pivot_table.index)

    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Return (%)', rotation=270, labelpad=20)

    # Add values to cells
    for i in range(len(pivot_table.index)):
        for j in range(len(pivot_table.columns)):
            value = pivot_table.iloc[i, j]
            if not pd.isna(value):
                text = plt.text(j, i, f'{value:.1f}%',
                               ha="center", va="center", color="black", fontsize=9)

    plt.title(f'Monthly Returns Heatmap - {ticker}', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Year', fontsize=12)
    plt.tight_layout()

    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Monthly returns heatmap saved to {save_path}")
    else:
        plt.show()

    plt.close()


def create_performance_summary(results, save_dir='charts'):
    """
    Create all performance charts for a backtest result

    Args:
        results: Dictionary returned by Backtester.run()
        save_dir: Directory to save charts
    """
    import os

    # Create charts directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    ticker = results['ticker']
    equity_curve = results['equity_curve']
    trades = results['trades']

    # Generate all charts
    print(f"\nGenerating performance charts for {ticker}...")

    plot_equity_curve(
        equity_curve,
        ticker,
        save_path=f'{save_dir}/{ticker}_equity_curve.png'
    )

    plot_drawdown(
        equity_curve,
        ticker,
        save_path=f'{save_dir}/{ticker}_drawdown.png'
    )

    plot_trade_distribution(
        trades,
        ticker,
        save_path=f'{save_dir}/{ticker}_trade_distribution.png'
    )

    plot_monthly_returns(
        equity_curve,
        ticker,
        save_path=f'{save_dir}/{ticker}_monthly_returns.png'
    )

    print(f"All charts saved to {save_dir}/")
