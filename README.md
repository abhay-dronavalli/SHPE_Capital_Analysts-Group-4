# Trading Algorithm - SHPE Capital Analysts

A Python-based trading algorithm that analyzes stocks using fundamental and technical indicators to generate buy/sell recommendations.

## Features

- **10 Comprehensive Indicators**
  - Valuation: PEG Ratio
  - Profitability: Operating Margin, Free Cash Flow
  - Growth: Revenue Growth, FCF Growth
  - Financial Health: Debt-to-Equity Ratio
  - Technical: Moving Averages (50/200), RSI, Volume
  - Market Conditions: VIX Filter

- **Scoring System**: Each indicator scored 0-5 points, totaling 0-50
- **Clear Recommendations**: STRONG BUY, BUY, HOLD, WEAK SELL, AVOID
- **Real-time Data**: Fetches data from Yahoo Finance via yfinance
- **Modular Design**: Clean, organized code structure for easy maintenance

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SHPE_Capital_Analysts.git
cd SHPE_Capital_Analysts
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Analyze a Single Stock
```bash
python main.py
```

This will analyze Apple (AAPL) and a few other stocks by default.

### Analyze Multiple Stocks
Edit `main.py`:
```python
from analysis.analyzer import analyze_stock
from utils.helpers import analyze_multiple_stocks, print_summary

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    results = analyze_multiple_stocks(tickers)
    print_summary(results)
```

### Example Output
```
Analyzing: AAPL
============================================================
Current Price: $150.25
50-day MA: $148.30
200-day MA: $145.60
RSI: 52.34
Volume Ratio: 1.15x
VIX: 18.45

INDICATOR SCORES (0-5 each):
1. PEG Ratio..................... 4.0
2. Operating Margin.............. 3.5
3. Free Cash Flow................ 5.0
4. Revenue Growth................ 4.0
5. FCF Growth.................... 3.5
6. Debt-to-Equity................ 4.0
7. Trend (MA50/200).............. 5.0
8. Momentum (RSI)................ 4.0
9. Volume........................ 3.5
10. VIX Filter................... 4.0
----------------------------------------
TOTAL SCORE...................... 40.5/50
PERCENTAGE....................... 81.0%

RECOMMENDATION: STRONG BUY
```

## Project Structure

```
SHPE_Capital_Analysts/
├── main.py                 # Entry point
├── config.py              # Configuration & constants
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore file
│
├── data/
│   └── data_fetcher.py   # Fetch data from yfinance
│
├── indicators/
│   ├── __init__.py
│   ├── technical.py      # Technical indicators
│   └── fundamental.py    # Fundamental indicators
│
├── scoring/
│   ├── __init__.py
│   └── scorer.py         # Scoring functions
│
├── analysis/
│   ├── __init__.py
│   └── analyzer.py       # Main analysis logic
│
└── utils/
    ├── __init__.py
    └── helpers.py        # Helper functions
```

## Scoring System

Each stock is evaluated on 10 indicators, each scored 0-5:

### Total Score Interpretation
- **40-50**: STRONG BUY
- **28-39**: BUY
- **18-27**: HOLD
- **8-17**: WEAK SELL
- **0-7**: AVOID

### Indicator Thresholds

#### Valuation
- **PEG Ratio**: Lower is better (5 pts if ≤1.5, 1 pt if >3.5)

#### Profitability
- **Operating Margin**: 5 pts if >10%, 1 pt if <1%
- **Free Cash Flow**: 5 pts if >10% of revenue, 1 pt if negative

#### Growth
- **Revenue Growth**: 5 pts if >10%, 1 pt if <0%
- **FCF Growth**: 5 pts if >10%, 1 pt if negative

#### Financial Health
- **Debt-to-Equity**: 5 pts if <0.5, 1 pt if >2.5

#### Technical
- **Trend (MA50/200)**: 5 pts if price above both, 1 pt if downtrend
- **Momentum (RSI)**: 5 pts if 35-55, 1 pt if >70
- **Volume**: 5 pts if >1.20x average, 1 pt if <0.8x

#### Market Conditions
- **VIX Filter**: 5 pts if <20, 1 pt if >35

## Configuration

Edit `config.py` to adjust:
- Moving average periods
- RSI period
- Volume comparison period
- Scoring thresholds
- Recommendation levels

## Limitations & Disclaimers

⚠️ **Important**: This algorithm is for educational purposes only. It is NOT financial advice.

- Past performance does not guarantee future results
- This tool analyzes historical data and current metrics only
- External factors (news, earnings, market events) are not accounted for
- Always do your own research before investing
- Consult a financial advisor before making investment decisions

## Future Enhancements

- [ ] Backtesting module
- [ ] Paper trading integration
- [ ] Real-time alerts
- [ ] Portfolio optimization
- [ ] Sentiment analysis
- [ ] Machine learning predictions
- [ ] Web dashboard

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Team

SHPE Capital Analysts - Group 4

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the team.

---

**Disclaimer**: This tool is provided for educational purposes only. We are not responsible for any financial losses. Always conduct thorough research and consult professionals before making investment decisions.
