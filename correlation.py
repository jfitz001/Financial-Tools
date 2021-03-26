import yfinance as yf
import pandas as pd


def mkt_correlation(ticker_list, market='QQQ', time='1y'):
    data = yf.download(ticker_list, period=time, interval='1d', group_by='ticker')
    market_data = pd.DataFrame(yf.Ticker(market).history(period=time, interval='1d')['Close'])
    new_data = []
    weights = 1 / len(ticker_list)
    cash = 1000000
    for i in ticker_list:
        stock_normal_ret = data[i]['Close'] / data[i].iloc[0]['Close']
        alloc = stock_normal_ret * weights
        balance = alloc * cash
        new_data.append(balance)
    stocks = pd.concat(new_data, axis=1)
    portfolio = stocks.sum(axis=1)
    correlation = portfo
