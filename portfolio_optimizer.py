# returns sharpe ratio and weights of a given portfolio
# accepts a list of stocks to compute the max sharpe

from yahooquery import Ticker
import yfinance as yf
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns


def max_sharpe(ticker, period='1y', interval='1d'):
    x = Ticker(ticker, retry=20, status_forcelist=[404, 429, 500, 502, 503, 504])
    data = x.history(period=period, interval=interval)
    df = pd.DataFrame()
    df[ticker] = data['close']
    mu = expected_returns.mean_historical_return(df)
    s = risk_models.sample_cov(df)
    ef = EfficientFrontier(mu, s)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    x = ef.portfolio_performance(verbose=False)
    if x is None:
        return 0
    else:
        return round(2.5 * x[2] / 15, 3)  # sharpe adjusted weight


def max_sharpe_multi(ticker_list, time='1d', cash=10000000):
    data = yf.download(ticker_list, period='10y', interval=time)
    if len(ticker_list) > 1:
        data = yf.download(ticker_list, period='10y', interval=time, group_by='ticker')
    new_data = []
    df = pd.DataFrame()
    weight = 1 / len(ticker_list)
    for i in ticker_list:
        stock_normal_ret = data['Close'] / data.iloc[0]['Close']
        df[i] = data['Close']
        if len(ticker_list) > 1:
            stock_normal_ret = data[i]['Close'] / data[i].iloc[0]['Close']
            df[i] = data[i]['Close']
        alloc = stock_normal_ret * weight
        balance = alloc * cash
        new_data.append(balance)

    mu = expected_returns.mean_historical_return(df)
    s = risk_models.sample_cov(df)
    ef = EfficientFrontier(mu, s)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    x = ef.portfolio_performance(verbose=True)
    return cleaned_weights, round(2.5 * x[2] / 15, 3)  # sharpe adjusted weight


def min_variance(ticker_list, period='1y', interval='1d', cash=10000000):
    x = Ticker(ticker_list, retry=20, status_forcelist=[404, 429, 500, 502, 503, 504])
    data = x.history(period=period, interval=interval)
    if len(ticker_list) > 1:
        data = yf.download(ticker_list, period='10y', interval=interval, group_by='ticker')
    new_data = []
    df = pd.DataFrame()
    weight = 1 / len(ticker_list)
    for i in ticker_list:
        stock_normal_ret = data['close'] / data.iloc[0]['close']
        df[i] = data['close']
        if len(ticker_list) > 1:
            stock_normal_ret = data[i]['close'] / data[i].iloc[0]['close']
            df[i] = data[i]['close']
        alloc = stock_normal_ret * weight
        balance = alloc * cash
        new_data.append(balance)

    mu = expected_returns.mean_historical_return(df)
    s = risk_models.sample_cov(df)
    ef = EfficientFrontier(mu, s)
    weights = ef.min_volatility()
    sharpe = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    x = ef.portfolio_performance(verbose=False)
    return cleaned_weights, round(2.5 * x[2] / 15, 3)  # sharpe adjusted weight

def tqqq_sqqq_shares(ticker):
    if ticker == 'tqqq':
        return .75
    if ticker == 'sqqq':
        return .25


def vix_shares(ticker):
    return 1.0
