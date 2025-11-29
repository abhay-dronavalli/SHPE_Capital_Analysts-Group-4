import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data.data_fetcher import fetch_stock_data
from indicators.technical import calculate_moving_averages, calculate_rsi, calculate_volume_ratio, calculate_vix
from config import RECOMMENDATION_THRESHOLDS


class Backtester:
    def __init__(self, ticker, start_date, end_date, initial_capital=10000,
                 stop_loss_pct=0.07, max_position_pct=1.0, daily_loss_limit_pct=0.10):
        """
        Initialize backtester with risk management controls

        Args:
            ticker: Stock symbol
            start_date: Start date (e.g., "2020-01-01")
            end_date: End date (e.g., "2024-01-01")
            initial_capital: Starting investment
            stop_loss_pct: Maximum loss per trade before auto-exit (default 7%)
            max_position_pct: Maximum % of capital to invest per trade (default 100%)
            daily_loss_limit_pct: Circuit breaker - stop trading if daily loss exceeds this (default 10%)
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.trades = []
        self.equity_curve = []

        # Risk management parameters
        self.stop_loss_pct = stop_loss_pct
        self.max_position_pct = max_position_pct
        self.daily_loss_limit_pct = daily_loss_limit_pct
        self.daily_start_equity = initial_capital
        self.trading_halted = False  # Circuit breaker flag
        
    def generate_signals(self, price_data):
        """
        Generate buy/sell signals for each day
        
        Returns:
            DataFrame with signals added
        """
        # Calculate indicators
        ma50, ma200 = calculate_moving_averages(price_data['Close'])
        rsi = calculate_rsi(price_data['Close'])
        volume_ratio = calculate_volume_ratio(price_data['Volume'])
        
        # Add to dataframe
        price_data['MA50'] = ma50
        price_data['MA200'] = ma200
        price_data['RSI'] = rsi
        price_data['Volume_Ratio'] = volume_ratio
        
        # Generate simple signals based on technical indicators
        signals = []
        
        for i in range(len(price_data)):
            if pd.isna(price_data['MA200'].iloc[i]):
                signals.append('HOLD')
                continue
            
            score = 0
            price = price_data['Close'].iloc[i]
            ma50_val = price_data['MA50'].iloc[i]
            ma200_val = price_data['MA200'].iloc[i]
            rsi_val = price_data['RSI'].iloc[i]
            vol_ratio = price_data['Volume_Ratio'].iloc[i]
            
            # Score trend (0-3 points)
            if price > ma50_val and price > ma200_val:
                score += 3  # Strong uptrend
            elif price > ma50_val:
                score += 2  # Uptrend
            elif price > ma200_val:
                score += 1  # Weak uptrend
            
            # Score RSI (0-2 points)
            if not pd.isna(rsi_val):
                if 30 < rsi_val < 70:
                    score += 2  # Good range
                elif rsi_val < 30:
                    score += 1  # Oversold (potential bounce)
            
            # Score volume (0-1 point)
            if not pd.isna(vol_ratio) and vol_ratio > 1.0:
                score += 1
            
            # Generate signal (max score = 6)
            if score >= 5:
                signals.append('BUY')
            elif score >= 3:
                signals.append('HOLD')
            else:
                signals.append('SELL')
        
        price_data['Signal'] = signals
        return price_data
    
    def simulate_trades(self, price_data):
        """
        Simulate trading based on signals with risk management controls

        Args:
            price_data: DataFrame with prices and signals

        Returns:
            Final portfolio value
        """
        position = None  # Current position (shares held)
        entry_price = 0
        entry_date = None

        for i in range(len(price_data)):
            date = price_data.index[i]
            current_price = price_data['Close'].iloc[i]
            signal = price_data['Signal'].iloc[i]

            # Calculate current equity
            if position is not None:
                equity = self.cash + (position * current_price)
            else:
                equity = self.cash

            # Check daily loss limit (circuit breaker)
            if i > 0 and equity < self.daily_start_equity * (1 - self.daily_loss_limit_pct):
                if not self.trading_halted:
                    print(f"\n[!] CIRCUIT BREAKER TRIGGERED on {date.date()}")
                    print(f"    Daily loss exceeded {self.daily_loss_limit_pct*100}%. Trading halted for the day.")
                    self.trading_halted = True
            else:
                # Reset circuit breaker at start of new day
                if self.trading_halted:
                    self.trading_halted = False
                    self.daily_start_equity = equity

            self.equity_curve.append({
                'date': date,
                'equity': equity,
                'signal': signal
            })

            # RISK CONTROL: Check stop-loss on existing position
            stop_loss_triggered = False
            if position is not None:
                position_loss_pct = (current_price - entry_price) / entry_price
                if position_loss_pct <= -self.stop_loss_pct:
                    # Stop-loss triggered - force sell
                    signal = 'SELL'
                    stop_loss_triggered = True
                    print(f"\n[X] STOP-LOSS TRIGGERED on {date.date()} | Loss: {position_loss_pct*100:.2f}%")

            # BUY signal
            if signal == 'BUY' and position is None and self.cash > 0 and not self.trading_halted:
                # RISK CONTROL: Position sizing - limit investment amount
                max_investment = self.cash * self.max_position_pct
                position = max_investment / current_price
                entry_price = current_price
                entry_date = date
                self.cash = self.cash - max_investment  # Deduct invested amount

                print(f"BUY:  {date.date()} | Price: ${current_price:.2f} | Shares: {position:.2f} | Investment: ${max_investment:.2f}")

            # SELL signal (includes stop-loss triggered sells)
            elif signal == 'SELL' and position is not None:
                # Sell all shares
                exit_price = current_price
                proceeds = position * exit_price
                profit = proceeds - (position * entry_price)
                profit_pct = (profit / (position * entry_price)) * 100

                sell_reason = "STOP-LOSS" if stop_loss_triggered else "SIGNAL"

                self.trades.append({
                    'entry_date': entry_date,
                    'entry_price': entry_price,
                    'exit_date': date,
                    'exit_price': exit_price,
                    'shares': position,
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'exit_reason': sell_reason
                })

                self.cash = self.cash + proceeds
                position = None

                print(f"SELL: {date.date()} | Price: ${exit_price:.2f} | Profit: ${profit:.2f} ({profit_pct:.2f}%) | Reason: {sell_reason}")
        
        # Close position at end if still holding
        if position is not None:
            final_price = price_data['Close'].iloc[-1]
            final_date = price_data.index[-1]
            proceeds = position * final_price
            profit = proceeds - (position * entry_price)
            profit_pct = (profit / (position * entry_price)) * 100

            self.trades.append({
                'entry_date': entry_date,
                'entry_price': entry_price,
                'exit_date': final_date,
                'exit_price': final_price,
                'shares': position,
                'profit': profit,
                'profit_pct': profit_pct,
                'exit_reason': 'END_OF_PERIOD'
            })

            self.cash = self.cash + proceeds
            print(f"SELL: {final_date.date()} | Price: ${final_price:.2f} | Profit: ${profit:.2f} ({profit_pct:.2f}%) | Reason: END_OF_PERIOD")

        return self.cash
    
    def calculate_metrics(self):
        """
        Calculate comprehensive performance metrics including risk-adjusted returns

        Returns:
            Dictionary of metrics
        """
        if not self.trades:
            return None

        # Total return
        final_value = self.cash
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100

        # CAGR (Compound Annual Growth Rate)
        start_date_obj = pd.to_datetime(self.start_date)
        end_date_obj = pd.to_datetime(self.end_date)
        years = (end_date_obj - start_date_obj).days / 365.25
        cagr = ((final_value / self.initial_capital) ** (1 / years) - 1) * 100

        # Win rate
        winning_trades = [t for t in self.trades if t['profit'] > 0]
        win_rate = (len(winning_trades) / len(self.trades)) * 100

        # Average profit per trade
        total_profit = sum(t['profit'] for t in self.trades)
        avg_profit = total_profit / len(self.trades)

        # Max drawdown
        equity_values = [e['equity'] for e in self.equity_curve]
        peak = equity_values[0]
        max_drawdown = 0

        for value in equity_values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        # Sharpe Ratio (risk-adjusted return metric)
        # Calculate daily returns
        equity_series = pd.Series(equity_values)
        daily_returns = equity_series.pct_change().dropna()

        if len(daily_returns) > 0 and daily_returns.std() > 0:
            # Annualized Sharpe Ratio (assuming 252 trading days per year)
            # Risk-free rate assumed to be 2% annually (0.02/252 daily)
            risk_free_rate_daily = 0.02 / 252
            excess_returns = daily_returns - risk_free_rate_daily
            sharpe_ratio = np.sqrt(252) * (excess_returns.mean() / daily_returns.std())
        else:
            sharpe_ratio = 0

        # Sortino Ratio (only penalizes downside volatility)
        downside_returns = daily_returns[daily_returns < 0]
        if len(downside_returns) > 0 and downside_returns.std() > 0:
            sortino_ratio = np.sqrt(252) * (daily_returns.mean() - risk_free_rate_daily) / downside_returns.std()
        else:
            sortino_ratio = 0

        # Best and worst trades
        best_trade = max(self.trades, key=lambda x: x['profit_pct'])
        worst_trade = min(self.trades, key=lambda x: x['profit_pct'])

        # Count stop-loss triggered trades
        stop_loss_trades = [t for t in self.trades if t.get('exit_reason') == 'STOP-LOSS']
        stop_loss_count = len(stop_loss_trades)

        return {
            'final_value': final_value,
            'total_profit': total_profit,
            'total_return': total_return,
            'cagr': cagr,
            'num_trades': len(self.trades),
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'best_trade': best_trade,
            'worst_trade': worst_trade,
            'stop_loss_count': stop_loss_count
        }
    
    def run(self, verbose=True):
        """
        Run the backtest
        
        Returns:
            Dictionary with results
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"BACKTESTING: {self.ticker}")
            print(f"Period: {self.start_date} to {self.end_date}")
            print(f"Initial Capital: ${self.initial_capital:,.2f}")
            print(f"{'='*70}\n")
        
        # Fetch data
        price_data = fetch_stock_data(self.ticker, period="10y")
        price_data = price_data[self.start_date:self.end_date]
        
        if price_data.empty:
            print(f"Error: No data available for {self.ticker}")
            return None
        
        # Generate signals
        price_data = self.generate_signals(price_data)
        
        if verbose:
            print("Trade Log:")
            print("-" * 70)
        
        # Simulate trades
        final_value = self.simulate_trades(price_data)
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        
        if metrics is None:
            print("\nNo trades were executed!")
            print("The algorithm may be too conservative or data is insufficient.")
            return None
        
        # Print results
        if verbose:
            print("\n" + "="*70)
            print("RESULTS")
            print("="*70)
            print(f"Final Account Value:     ${metrics['final_value']:,.2f}")
            print(f"Total Profit/Loss:       ${metrics['total_profit']:,.2f}")
            print(f"Total Return:            {metrics['total_return']:.2f}%")
            print(f"CAGR:                    {metrics['cagr']:.2f}%")
            print(f"\nRisk-Adjusted Performance:")
            print(f"Sharpe Ratio:            {metrics['sharpe_ratio']:.3f}")
            print(f"Sortino Ratio:           {metrics['sortino_ratio']:.3f}")
            print(f"Max Drawdown:            {metrics['max_drawdown']:.2f}%")
            print(f"\nTrading Statistics:")
            print(f"Number of Trades:        {metrics['num_trades']}")
            print(f"Win Rate:                {metrics['win_rate']:.2f}%")
            print(f"Average Profit/Trade:    ${metrics['avg_profit']:,.2f}")
            print(f"Stop-Loss Exits:         {metrics['stop_loss_count']}")
            print(f"\nBest Trade:              {metrics['best_trade']['profit_pct']:.2f}% on {metrics['best_trade']['exit_date'].date()}")
            print(f"Worst Trade:             {metrics['worst_trade']['profit_pct']:.2f}% on {metrics['worst_trade']['exit_date'].date()}")
            print("="*70 + "\n")
        
        return {
            'ticker': self.ticker,
            'metrics': metrics,
            'trades': self.trades,
            'equity_curve': self.equity_curve
        }