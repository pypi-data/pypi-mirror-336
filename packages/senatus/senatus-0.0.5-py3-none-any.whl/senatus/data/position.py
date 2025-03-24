import pandas as pd

class Position():
    def __init__(
            self,
            symbol: str,
            is_open: bool,
            type: str,
            position_side: str,
            position_size: float,
            entry_price: float,
            open_timeframe: pd.Timestamp,
            close_timeframe: pd.Timestamp = None,
            close_price: float = None
        ):
        self.symbol = symbol
        self.is_open = is_open
        self.open_timeframe = open_timeframe
        self.close_timeframe = close_timeframe
        self.type = type
        self.position_side = position_side
        self.position_size = position_size
        self.entry_price = entry_price
        self.close_price = close_price

    def get_unrealized_pnl(self):
        unrealized_pnl = (self.current_price - self.entry_price) * self.position_size
        if self.position_side == "SHORT":
            unrealized_pnl *= -1
        return unrealized_pnl
    
    def close_position(self, close_price, close_timeframe):
        self.close_price = close_price
        self.close_timeframe = close_timeframe
        self.is_open = False
        return self
    
    def get_pnl(self):
        if self.is_open: return 0
        pnl = (self.current_price - self.entry_price) * self.position_size
        if self.position_side == "SHORT":
            pnl *= -1
        return pnl


