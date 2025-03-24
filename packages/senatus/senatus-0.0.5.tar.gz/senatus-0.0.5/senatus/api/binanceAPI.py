import pandas as pd
from binance.um_futures import UMFutures
from ..data import Candlestick, PriceSeries

def processRawCandlestickData(rawCD: list) -> list[Candlestick]:
    """
    Transforms raw data from Binance kline API to Candlestick type
    """

    return [
        Candlestick(
            timestamp = pd.Timestamp(cd[0], unit='ms'),
            open = cd[1],
            high = cd[2],
            low = cd[3],
            close = cd[4],
            volume = cd[5],
        ) for cd in rawCD
    ]


def getPastCandlesTimeSeries(pair: str, timeframe: str) -> PriceSeries:
    """
    Request Binance API kline data and returns a Pandas DataFrame with Candlesticks
    """

    um_futures_client = UMFutures()
    pastCandleSticks = um_futures_client.klines(pair, timeframe, limit=1000)
    priceSeries = PriceSeries(processRawCandlestickData(pastCandleSticks), pair, timeframe)
    return priceSeries