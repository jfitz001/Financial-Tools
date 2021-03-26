# module for identifying the CVAR (expected shortfall) of a portfolio
import yfinance as yf
import pandas as pd


def value_at_risk(returns, confidence_level=.05):
    """
    It calculates the Value at Risk (VaR) of some time series. It represents
    the maximum loss with the given confidence level.
    """
    # Calculating VaR
    return returns.quantile(confidence_level, axis=0, interpolation='higher')


def expected_shortfall(returns, confidence_level=.05):
    """
    It calculates the Expected Shortfall (ES) of some time series. It represents
    the average loss according to the Value at Risk.
    """
    # Calculating VaR
    var = value_at_risk(returns, confidence_level)

    # ES is the average of the worst losses (under var)
    return var, returns[returns.lt(var, axis=1)].mean()


def conditional_var(ticker_list, time='1d', confidence_level=0.05, k=.02):
    data = yf.download(ticker_list, period='10y', interval=time, group_by='ticker')
    # data = yf.download(ticker_list, period='10y', interval=time)['Close']
    df = pd.DataFrame(data)
    # ticker_returns = df.copy().pct_change().dropna(axis=0).rename(columns={'Close': 'dr1'})
    for i in ticker_list:
        # stock_normal_ret = data[i]['Close'] / data[i].iloc[0]['Close']
        df[i] = data[i]['Close']
        ticker_returns = df[i].copy().pct_change().dropna(axis=0).rename(columns={'Close': 'dr1'})
    # ticker_returns = data['Close'] / data.iloc[0]['Close']
        ticker_returns[i]['dr2'] = ticker_returns[i]['dr1'].copy()
        ticker_returns.loc[ticker_returns[i]['dr1'] < ticker_returns[i]['dr1'].quantile(confidence_level), 'dr2'] -= k

    # Getting ES using expected_shortfall function
    es = expected_shortfall(ticker_returns)
    return es[0]['dr1'], es[1]['dr1']
