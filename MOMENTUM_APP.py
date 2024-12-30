import yfinance as yf 
from yahoo_fin.stock_info import *
## Standard Python Data Science stack
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import math
import statsmodels.api as sm
import datetime as dt
import math
from scipy.optimize import minimize
from scipy.stats import (norm as norm, linregress as linregress)
plt.rcParams['figure.figsize'] = [20, 10]
#from SHARPR_backend import *
from fredapi import Fred
fred = Fred(api_key='3cc2743ce40daec36ca56954fefedca7')
from FedTools import MonetaryPolicyCommittee
from FedTools import BeigeBooks
from FedTools import FederalReserveMins
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import ceil
from MOMENTR import *


##LOAD THIS
all_m_ret = pd.read_csv("all_monthly_returns.csv", index_col=0, parse_dates=True)
all_m_ret.index = pd.to_datetime(all_m_ret.index)
all_w_ret = pd.read_csv("all_weekly_returns.csv", index_col=0, parse_dates=True)
all_w_ret.index = pd.to_datetime(all_w_ret.index)


## HERE THE PARAMETER ENTRY BEGINS
benchmark = yf.download('SPY', start = '2010-01-01')['Adj Close'] ###I want to populate 'SPY' with 'SPY' as default
benchmark.columns = ['Benchmark']

risk_free = yf.download('BIL', start = '2010-01-01')['Adj Close'] ###I want to populate 'BIL' with 'BIL' as default
risk_free.columns = ['Risk Free Return']

benchmark_m = benchmark.pct_change(fill_method=None).resample('ME').agg(lambda x: (x + 1).prod() - 1).dropna()
benchmark_w = benchmark.pct_change(fill_method=None).resample('W').agg(lambda x: (x + 1).prod() - 1).dropna()
risk_free_m = risk_free.pct_change(fill_method=None).resample('ME').agg(lambda x: (x + 1).prod() - 1).dropna()
risk_free_w = risk_free.pct_change(fill_method=None).resample('W').agg(lambda x: (x + 1).prod() - 1).dropna()

lookback_periods=(12,8,4) #I want to populate these three arguments
top_counts=(30,25,10) #I want to populate these three arguments
holding_length=1 #I want to populate this argument


#if "weekly"
returns = all_w_ret
benchmark = benchmark_w
#if "monthly"
returns = all_m_ret
benchmark = benchmark_m

#"RUN ANALYSIS"-BUTTON EXECUTES THIS
backtest = triple_momentum_filter(returns=returns, lookback_periods=lookback_periods, top_counts=top_counts, holding_length=holding_length)
rolling_cumulative_return = calc_rolling_cum_ret(backtest["Strategy Return"])
tickers_to_plot = get_latest_picks_triple(returns,lookback_periods = lookback_periods,top_counts = top_counts)

#SHOW THESE THREE PLOTS. THEY ARE PLOTLY FUNCTIONS
plot_cumulative_returns(backtest["Strategy Return"], benchmark_w)
plot_rolling_cumulative_return(rolling_cumulative_return)
plot_top_stocks(returns = returns,lookbacks=lookback_periods,tickers_to_plot = tickers_to_plot)