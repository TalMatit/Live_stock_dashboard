import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

def Fetch(ticker):
    """ Fetches the info on the requested ticker and stores it in streamlit
    in the session state. returns ticker info as a dictionary and a ticker object for
    later proccessing.
    """

    ticker_object = yf.Ticker(ticker.lower())
    ticker_info = ticker_object.info
    
    return(ticker_info, ticker_object)

def History(ticker_object, interval):
    """ Fetches the ticker's trading history for the with the requested interval.
    returns a list of trading dates and a history pandas data frame that can be parsed for the streamlit
    interface.
    """
    history = ticker_object.history(period='max', interval=interval)
    dates_datetime = pd.DataFrame(history.index)
    dates_raw = pd.DataFrame(history.index.to_list())
    dates_raw[0] = dates_raw[0].astype(str) 

    dates = []

    for date in dates_raw[0]:
        dates.append(date[:10])

    return(dates, dates_datetime, history)


if __name__ == "__main__":
    info , ticker = Fetch("AAPL")
    dates, datetime,  history = History(ticker, interval='1mo')
    print(datetime)