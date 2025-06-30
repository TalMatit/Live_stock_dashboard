import yfinance as yf
import streamlit as st
from curl_cffi import CurlError
import pandas as pd
import plotly.graph_objects as go
import functions

# Declaring session_state variables:
if 'dates' not in st.session_state:
    st.session_state.dates = []
if 'stock_ticker' not in st.session_state:
    st.session_state.stock_ticker = ''
if 'ticker_info' not in st.session_state:
    st.session_state.ticker_info = {}
if 'history' not in st.session_state:
    st.session_state.history = ''
if 'show_data' not in st.session_state:
    st.session_state.show_data = False
if 'period' not in st.session_state:
    st.session_state.period = ''
if 'interval' not in st.session_state:
    st.session_state.interval = '1mo'
if 'period_data' not in st.session_state:
    st.session_state.period_data = st.session_state.history
if 'clean_period' not in st.session_state:
    st.session_state.clean_period = ()
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = st.session_state.clean_period


INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

# Setting the retrieved data from the Fetch function into cache
@st.cache_resource
def Fetch_info(ticker):
    Fetch = functions.Fetch(ticker)
    return Fetch

# Setting the retrieved data from the History function into cache
@st.cache_resource()
def Get_history(_ticker, interval):
    History = functions.History(ticker_object=_ticker, interval=interval)
    return History

# Creating an initialization function (allows the user to input his desired ticker)
def initialization():
    # Adding a title to the website
    st.title("Live Stock Dashboard")

    # Enabling the user to enter a stock ticker of his choice to get data on
    st.header("Enter stock ticker")
    upper_columns = st.columns([4,1])
    with upper_columns[0]:
        st.session_state.stock_ticker = st.text_input(label=".", label_visibility="hidden")

    with upper_columns[1]:
        st.caption("")
        st.caption("")
        search = st.button(label = "Search", icon = "🔍")

    if search:
        try:
            st.session_state.ticker_info, st.session_state.ticker_object = Fetch_info(st.session_state.stock_ticker)
            
            # Checking if the user entered a valid stock ticker
            if st.session_state.ticker_info.get("displayName") == None:
                st.error(f"Could not find a valid stock with the name '{st.session_state.stock_ticker.upper()}'", icon="🚨")
            else:
                st.session_state.show_data = True
        
        # Handling expected errors
        except CurlError as e:
            st.error("A network error occurred. This could be due to an invalid ticker or a temporary network issue.")

        except Exception as e:
            st.error(f"An error occured: {e}")
        return st.session_state.show_data


initialization()
# Showing the stock's basic overview
if st.session_state.show_data:
    st.subheader("Quick overview")
    stockinfo_columns = st.columns(2)
    with stockinfo_columns[0]:
        st.text(f"Coumpany name: {st.session_state.ticker_info.get("displayName")}")
        st.text(f"Country: {st.session_state.ticker_info.get("country")}")
        st.text(f"Website: {st.session_state.ticker_info.get("website")}")

    with stockinfo_columns[1]:
        st.text(f"Sector:  {st.session_state.ticker_info.get("sectorDisp")}")
        st.text(f"Coumpany CEO: {st.session_state.ticker_info.get("companyOfficers")[0]["name"]}")

    # Adding an option for the user to choose his desired candlestick interval
    st.session_state.interval = st.select_slider(label="Choose desired interval", options=INTERVALS, value=INTERVALS[-1])

    # Getting trading data on the stock for the past month
    st.session_state.dates, st.session_state.period, st.session_state.history, = Get_history(_ticker=st.session_state.ticker_object, interval=st.session_state.interval)
    
    #Cleaning up the Timestamp period, and making sure that the period selection slider stays with desired selection.
    if st.session_state.clean_period == ():
        st.session_state.clean_period = functions.clean_timestamp(st.session_state.period)
        st.session_state.selected_period = st.session_state.clean_period
        
    # Creating slider for the user to choose viewing period
    st.session_state.selected_period = st.select_slider(label="Choose desired period", options=st.session_state.clean_period,
                                                value=(st.session_state.selected_period[0], st.session_state.selected_period[-1]))
    
    # Creating the stock trading data frame with the desired parameters
    st.session_state.period_data = st.session_state.history[st.session_state.selected_period[0]:st.session_state.selected_period[1]]

    st.write(f"Requested period: {st.session_state.selected_period}")
    st.write(f"Requested interval {st.session_state.interval}")
    
    
    # Generating Candlestick chart to be shown on the webpage
    candlestick = go.Figure(data=[go.Candlestick(x=st.session_state.period_data.index,
                                                open=st.session_state.period_data["Open"],
                                                close=st.session_state.period_data["Close"],
                                                high=st.session_state.period_data["High"],
                                                low=st.session_state.period_data["Low"])])
    
    st.plotly_chart(candlestick)
    

    st.subheader(f"Coumpany Description")
    st.text(st.session_state.ticker_info.get("longBusinessSummary"))
        
        
    
        



