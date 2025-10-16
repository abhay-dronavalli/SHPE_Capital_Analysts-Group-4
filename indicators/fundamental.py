import pandas as pd
from data.data_fetcher import fetch_quarterly_financials


def calculate_revenue_growth(ticker):
    """
    Calculate year-over-year revenue growth
    
    Returns:
        Revenue growth percentage
    """
    quarterly_financials, _ = fetch_quarterly_financials(ticker)
    
    if quarterly_financials.empty:
        return 0
    
    try:
        current_revenue = quarterly_financials.loc['Total Revenue'].iloc[0]
        previous_revenue = quarterly_financials.loc['Total Revenue'].iloc[4]
        
        if previous_revenue == 0:
            return 0
        
        growth = ((current_revenue - previous_revenue) / previous_revenue) * 100
        return growth
    except:
        return 0


def calculate_fcf_growth(ticker):
    """
    Calculate year-over-year free cash flow growth
    
    Returns:
        FCF growth percentage
    """
    _, cash_flow = fetch_quarterly_financials(ticker)
    
    if cash_flow.empty:
        return 0
    
    try:
        current_fcf = cash_flow.loc['Operating Cash Flow'].iloc[0] - cash_flow.loc['Capital Expenditures'].iloc[0]
        previous_fcf = cash_flow.loc['Operating Cash Flow'].iloc[4] - cash_flow.loc['Capital Expenditures'].iloc[4]
        
        if previous_fcf == 0:
            return 0
        
        growth = ((current_fcf - previous_fcf) / previous_fcf) * 100
        return growth
    except:
        return 0