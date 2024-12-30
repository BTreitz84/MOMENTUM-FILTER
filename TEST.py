import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
from MOMENTR import *  

all_m_ret = pd.read_csv(r"C:\Users\User\Desktop\GLADIO\MOMENTUM APP\all_monthly_returns.csv", index_col=0, parse_dates=True)
all_m_ret.index = pd.to_datetime(all_m_ret.index)
all_w_ret = pd.read_csv(r"C:\Users\User\Desktop\GLADIO\MOMENTUM APP\all_weekly_returns.csv", index_col=0, parse_dates=True)
all_w_ret.index = pd.to_datetime(all_w_ret.index)

@st.cache_data
def load_benchmark_and_rf():
    benchmark = yf.download('SPY', start='2010-01-01')[['Adj Close']]
    benchmark.columns = ["Benchmark"]
    risk_free = yf.download('BIL', start='2010-01-01')[['Adj Close']]
    risk_free.columns = ["Risk Free Return"]
    benchmark_m = benchmark.pct_change().resample('ME').apply(lambda x: (x + 1).prod() - 1).dropna()
    benchmark_w = benchmark.pct_change().resample('W').apply(lambda x: (x + 1).prod() - 1).dropna()
    risk_free_m = risk_free.pct_change().resample('ME').apply(lambda x: (x + 1).prod() - 1).dropna()
    risk_free_w = risk_free.pct_change().resample('W').apply(lambda x: (x + 1).prod() - 1).dropna()
    return benchmark_m, benchmark_w, risk_free_m, risk_free_w

benchmark_m, benchmark_w, risk_free_m, risk_free_w = load_benchmark_and_rf()

st.title("Triple Momentum Filter Backtest")

st.sidebar.header("Backtest Parameters")
frequency = st.sidebar.selectbox("Select Frequency", ["Weekly", "Monthly"], index=0)
returns = all_w_ret if frequency == "Weekly" else all_m_ret
benchmark = benchmark_w if frequency == "Weekly" else benchmark_m
freq = 52 if frequency == "Weekly" else 12

lookback_periods = st.sidebar.text_input("Lookback Periods (comma-separated)", "12,8,4")
lookback_periods = tuple(map(int, lookback_periods.split(",")))

top_counts = st.sidebar.text_input("Top Counts (comma-separated)", "50,25,10")
top_counts = tuple(map(int, top_counts.split(",")))

holding_length = st.sidebar.number_input("Holding Length", min_value=1, value=1)

if st.sidebar.button("Run Analysis"):
    backtest = triple_momentum_filter(
        returns=returns,
        lookback_periods=lookback_periods,
        top_counts=top_counts,
        holding_length=holding_length)

    rolling_cumulative_return = calc_rolling_cum_ret(backtest["Strategy Return"],freq=freq)
    tickers_to_plot = get_latest_picks_triple(
        returns,
        lookback_periods=lookback_periods,
        top_counts=top_counts)

    st.subheader("Backtest Results")
    st.write("### Strategy Returns")
    strat_fig = plot_cumulative_returns(backtest["Strategy Return"], benchmark)
    st.plotly_chart(strat_fig)

    st.write("### Rolling Cumulative Returns")
    rolling_fig = plot_rolling_cumulative_return(rolling_cumulative_return)
    st.plotly_chart(rolling_fig)

    st.write("### Top Stocks")
    top_stocks_fig = plot_top_stocks(returns=returns, lookbacks=lookback_periods, tickers_to_plot=tickers_to_plot)
    st.plotly_chart(top_stocks_fig)
