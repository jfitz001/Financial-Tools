import robin_stocks as rb
#from ...credentials import login
import datetime
import pandas as pd
import os

# robin stocks initialization
#rb.robinhood.login(login['username'], login['password'])

today = datetime.date.today()
monday = (today + datetime.timedelta((0 - today.weekday()) % 7))
wednesday = (today + datetime.timedelta((2 - today.weekday()) % 7))
friday = (today + datetime.timedelta((4 - today.weekday()) % 7))


def option_append(ticker, time, n_weeks):
    # requires a start date to loop through as well as number of weeks to continue to fetch prices
    # df initialization
    df = pd.DataFrame()
    for i in range(1, n_weeks):
        # date modification for robin stocks
        next_friday = time + datetime.timedelta(days=7*(i-1))
        next_friday = next_friday.strftime('%Y-%m-%d')

        # robin stocks function for options
        x = rb.robinhood.options.find_options_by_expiration(ticker, expirationDate=next_friday)

        # appends to the existing df
        df = df.append(pd.DataFrame.from_dict(x))

    # makes a date column with the same date for all options
    df['date'] = datetime.datetime.now()

    # removes the number index
    df.set_index('date', inplace=True)

    # saves as the ticker passed (APPENDS)
    if os.path.exists(f'{ticker}_options.csv'):
        df.to_csv(f'{ticker}_options.csv', mode='a', header=False)
    else:
        # if has not been made, creates file
        df.to_csv(f'{ticker}_options.csv')


option_append('MSFT', friday, 1)
