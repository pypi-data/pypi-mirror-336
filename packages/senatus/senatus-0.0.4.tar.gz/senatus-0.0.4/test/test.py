from senatus.api.binanceAPI import (getPastCandlesTimeSeries)
from senatus.data.indicators import (getMAV, getEMA, getWRSI)
from senatus.plotting.plotting import Plotting
from senatus.trader import TestTrader
from senatus.strategies import RSI_Margins_Strategy

#Params
pair = 'bnbusdt'
timeframe = '1h'

#Get past data
priceSeries = getPastCandlesTimeSeries(pair, timeframe)

#Subscribe to stream data

#Plot data
my_plot = Plotting(priceSeries)

my_plot.plot_asset_chart()

wrsi = getWRSI(priceSeries, 8)

my_plot.plot_indicator_dif_chart(wrsi)


tt = TestTrader(priceSeries, 1000)
tt.operate_strategy(wrsi, RSI_Margins_Strategy(15, 80), my_plot)

my_plot.apply_custom().show()