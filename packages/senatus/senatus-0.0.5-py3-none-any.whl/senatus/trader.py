import pandas as pd
from .data import PriceSeries
from .plotting import Plotting
from .data import Position
from .strategies import Strategy



class TestTrader:

    def __init__( 
            self,
            ps: PriceSeries,
            initial_margin: float
        ):
        self.df = ps.candles
        self.initial_margin = initial_margin
        self.open_positions: list[Position] = []

    def open_position(self, new_position: Position):
        self.open_positions.append(new_position)
        return self.open_positions[-1]

    def close_position(self, p_timeframe):
        return next((pos for pos in self.open_positions if pos.open_timeframe == p_timeframe), None)
    
    def operate_strategy(self, ind, strategy: Strategy, plot: Plotting):
        for i in range(len(self.df)):
            resp = strategy.check_condition(ind[0:i])
            if(resp.count('OPEN_LONG')):
                pos = self.open_position(Position(
                    symbol='btcusd',
                    is_open=True,
                    type='spot',
                    position_side='LONG',
                    position_size=1,
                    entry_price=self.df['close'].iat[i],
                    open_timeframe=self.df.index[i]
                ))
                plot.plotPosition(pos)
            if(resp.count('CLOSE_LONG')):
                pos = self.open_position(Position(
                    symbol='btcusd',
                    is_open=True,
                    type='spot',
                    position_side='SHORT',
                    position_size=1,
                    entry_price=self.df['close'].iat[i],
                    open_timeframe=self.df.index[i]
                ))
                plot.plotPosition(pos)
        
