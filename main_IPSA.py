import streamlit as st
import pandas as pd
import altair as alt
import statsmodels.api as sm
import yfinance as yf

data = yf.Ticker("^IPSA").history(period="1y") 
st.write(data.head())
