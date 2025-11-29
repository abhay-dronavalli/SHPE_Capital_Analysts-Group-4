# Algorithmic Trading System - Group 4
## SHPE Capital Analysts

A momentum-based algorithmic trading system that combines technical and fundamental analysis to identify high-quality stock investment opportunities.

---

## Table of Contents
1. [Algorithmic Trading Concepts Used](#algorithmic-trading-concepts-used)
2. [Strategy Overview](#strategy-overview)
3. [Risk Management](#risk-management)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Scoring System](#scoring-system)

---

## Algorithmic Trading Concepts Used

### 1. Market Data Feed
Our algorithm uses real-time and historical market data fetched via the yfinance API. The data includes:
- Price data (Open, High, Low, Close)
- Volume information
- Fundamental metrics (P/E ratio, revenue, free cash flow, debt levels)
- Market volatility index (VIX)

The algorithm processes this data to calculate technical indicators (moving averages, RSI) and fundamental scores, which drive our trading decisions.

### 2. Trading Platform & Execution
While this is a backtesting simulation, the system is designed to mimic real-world trading platforms. Our backtester simulates order execution by:
- Placing market orders at the next day's close price
- Tracking cash and position balances
- Calculating equity curves over time
- Enforcing risk management rules before execution

### 3. Connectivity & Latency
In production algorithmic trading, low latency is critical for execution speed. Our system acknowledges this by:
- Using efficient data structures (pandas DataFrames) for fast computations
- Pre-calculating indicators to minimize decision time
- Designing modular code that could interface with real-time data feeds
- While our backtest uses daily data, the architecture supports higher-frequency data

### 4. Backtesting Importance
Backtesting allows us to validate our strategy on historical data before risking real capital. Our backtester:
- Tests the strategy on 4+ years of historical data
- Calculates key performance metrics (total return, CAGR, win rate, Sharpe ratio, max drawdown)
- Identifies potential weaknesses and overfitting
- Provides visual feedback through equity curves and performance charts

This helps us understand how the strategy would have performed in different market conditions (bull markets, bear markets, high volatility periods).

### 5. Risk Controls
Risk management is embedded directly in the trading logic to prevent catastrophic losses:
- **Stop-Loss Orders**: Automatically exit positions when losses exceed 7% to limit downside
- **Position Sizing**: Never invest more than 100% of available capital
- **Maximum Drawdown Monitoring**: Track peak-to-trough declines to assess risk exposure
- **VIX Filter**: Avoid trading during extreme market volatility (VIX > 30)

These controls prevent the algorithm from taking excessive risk and protect against "blow-up" scenarios.

---

## Strategy Overview

### Core Philosophy
Our strategy identifies stocks with strong fundamentals AND positive technical momentum. We only buy when both conditions align, reducing false signals.

### Indicators Used
**Technical Indicators:**
- **50-day Moving Average (MA50)**: Short-term trend indicator
- **200-day Moving Average (MA200)**: Long-term trend indicator
- **Relative Strength Index (RSI)**: Momentum oscillator (14-day period)
- **Volume Ratio**: Current volume vs. 20-day average volume

**Fundamental Indicators:**
- PEG Ratio (valuation)
- Operating Margin (profitability)
- Free Cash Flow & FCF Growth (financial health)
- Revenue Growth (business growth)
- Debt-to-Equity Ratio (leverage risk)

### Time Windows
- **Daily Data**: The algorithm operates on daily closing prices
- **Lookback Periods**: 50 days (short-term), 200 days (long-term)
- **Backtesting Period**: 2020-2024 (4 years)

### Trading Rules

#### BUY Rules
The algorithm generates a BUY signal when the following conditions are met:
- **Trend Condition**: Price is above BOTH the 50-day and 200-day moving averages (strong uptrend)
- **Momentum Condition**: RSI is between 30 and 70 (not overbought/oversold)
- **Volume Condition**: Trading volume is above the 20-day average (confirms interest)
- **Overall Score**: Total score ≥ 5 out of 6 points (high conviction)
- **Risk Filter**: VIX < 30 (market volatility is manageable)
- **Position Check**: No existing position held (prevents over-concentration)

#### SELL Rules
The algorithm generates a SELL signal when:
- **Trend Breakdown**: Price falls below the 50-day moving average OR
- **Low Conviction**: Overall score drops below 3 points OR
- **Stop-Loss Triggered**: Position loss exceeds 7% from entry price OR
- **Overbought**: RSI exceeds 70 (momentum exhaustion)

#### HOLD Rules
The algorithm maintains the current position (no action) when:
- Already holding a position AND sell conditions are not met
- No position held AND buy conditions are not met (score between 3-4 points)
- VIX is elevated (25-30) indicating uncertain market conditions

---

## Risk Management

### 1. Stop-Loss Protection
- **Hard Stop**: Automatically exit any position with a loss exceeding 7%
- **Purpose**: Prevents small losses from becoming catastrophic losses
- **Implementation**: Checked on every trading day against entry price

### 2. Position Sizing
- **Maximum Position**: 100% of available capital per trade
- **Cash Management**: Tracks available cash to prevent over-leveraging
- **No Margin**: Algorithm does not use borrowed funds

### 3. Daily Loss Limit
- **Circuit Breaker**: Stops trading if daily account drawdown exceeds 10%
- **Purpose**: Prevents emotional spiral during extreme market events
- **Recovery**: Allows reassessment before resuming trading

### 4. Volatility Filter (VIX-based)
- **High Volatility**: When VIX > 30, no new positions are opened
- **Rationale**: Extreme volatility increases slippage and unpredictable price swings
- **Benefit**: Avoids trading during market crashes and panic selloffs

### Why These Controls Matter
- **Prevents Overfitting**: Stop-losses force discipline, preventing curve-fitting to historical data
- **Reduces Blow-Up Risk**: Position limits and daily loss caps prevent account destruction
- **Improves Risk-Adjusted Returns**: By avoiding high-volatility periods, we reduce drawdowns while maintaining upside capture

---

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd SHPE_Capital_Analysts-Group-4

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Running a Backtest
```python
from backtest.backtester import Backtester

# Create backtester instance
backtester = Backtester(
    ticker="AAPL",
    start_date="2020-01-01",
    end_date="2024-01-01",
    initial_capital=10000
)

# Run backtest
results = backtester.run()
```

### Analyzing a Stock
```python
from analysis.analyzer import analyze_stock

# Analyze current stock conditions
result = analyze_stock("MSFT")
```

### Multiple Stock Analysis
```python
from utils.helpers import analyze_multiple_stocks

tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
results = analyze_multiple_stocks(tickers)
```

---

## Project Structure

```
SHPE_Capital_Analysts-Group-4/
├── analysis/           # Stock analysis logic
│   └── analyzer.py     # Main analysis engine
├── backtest/          # Backtesting system
│   ├── backtester.py  # Core backtesting engine
│   └── metrics.py     # Performance metrics
├── data/              # Data fetching
│   └── data_fetcher.py # yfinance API wrapper
├── indicators/        # Technical & fundamental indicators
│   ├── technical.py   # MA, RSI, Volume calculations
│   └── fundamental.py # Growth metrics, FCF calculations
├── scoring/           # Scoring system
│   └── scorer.py      # Multi-factor scoring logic
├── utils/             # Helper functions
│   └── helpers.py     # Recommendations, batch processing
├── notebooks/         # Jupyter notebooks for analysis
├── config.py          # Configuration constants
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── README.md          # This file
```

---

## Scoring System

Our 10-factor scoring system evaluates each stock on a 0-50 point scale:

### Fundamental Factors (6 indicators)

#### 1. PEG Ratio
- 0 pts: >2.5 (overvalued)
- 1-2 pts: 1.8-2.5
- 3-4 pts: 1.0-1.8
- 5 pts: ≤1.0 (growth at reasonable price)

#### 2. Operating Margin (%)
- 0 pts: <0% (losing money on operations)
- 1-2 pts: 0-5% (barely profitable)
- 3-4 pts: 5-15% (good)
- 5 pts: >15% (excellent)

#### 3. Free Cash Flow (FCF)
- 0 pts: Negative or declining (red flag)
- 1-2 pts: Positive but flat
- 3-4 pts: Positive and growing >5% YoY
- 5 pts: Positive and growing >15% YoY

#### 4. Revenue Growth (YoY)
- 0 pts: <0% (shrinking)
- 1-2 pts: 0-5%
- 3-4 pts: 5-15%
- 5 pts: >15% (strong growth)

#### 5. Free Cash Flow Growth (YoY)
- 0 pts: Negative (worsening)
- 1-2 pts: 0-5%
- 3-4 pts: 5-15%
- 5 pts: >15%

#### 6. Debt-to-Equity (D/E) Ratio
- 0 pts: >2.5 (too much debt)
- 1-2 pts: 1.8-2.5
- 3-4 pts: 1.0-1.8
- 5 pts: <1.0 (low debt, safe)

### Technical Factors (4 indicators)

#### 7. Trend Identification (50/200 MA)
- 0 pts: Price < both MAs (downtrend)
- 1-2 pts: Price between MAs (transition)
- 3-4 pts: Price > 50-day, < 200-day (recovering)
- 5 pts: Price > both MAs (uptrend confirmed)

#### 8. Momentum Confirmation (RSI)
- 0 pts: RSI >70 (overbought, too late)
- 1-2 pts: RSI 60-70 (getting overheated)
- 3-4 pts: RSI 40-60 (neutral)
- 5 pts: RSI <40 (building from oversold)

#### 9. Volume Validation
- 0 pts: Volume <50% of average
- 1-2 pts: Volume near average
- 3-4 pts: Volume 10-25% above average
- 5 pts: >25% above average

#### 10. Market Volatility Filter (VIX)
- 0 pts: VIX >30 (avoid trading)
- 1-2 pts: VIX 25-30
- 3-4 pts: VIX 18-25
- 5 pts: VIX <18 (safe conditions)

### Recommendation Levels
- **40-50 pts**: Strong Buy
- **30-39 pts**: Buy
- **20-29 pts**: Hold
- **10-19 pts**: Weak Sell
- **0-9 pts**: Avoid

---

## License
This project is for educational purposes as part of the SHPE Capital Analysts program.
