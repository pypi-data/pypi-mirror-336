import numpy as np
import pandas as pd
from .data.position import Position
from typing import Callable, Optional


class Strategy:


    conditionToOpenLong: Optional[Callable[[pd.DataFrame, list[Position]], bool]]
    conditionToCloseLong: Optional[Callable[[pd.DataFrame, list[Position]], bool]]
    conditionToOpenShort: Optional[Callable[[pd.DataFrame, list[Position]], bool]]
    conditionToCloseShort:Optional[Callable[[pd.DataFrame, list[Position]], bool]]
    
    def __init__(
            self, 
            cOL: Optional[Callable[[pd.DataFrame, list[Position]], bool]] = lambda a, b: False, 
            cCL: Optional[Callable[[pd.DataFrame, list[Position]], bool]] = lambda a, b: False, 
            cOS: Optional[Callable[[pd.DataFrame, list[Position]], bool]] = lambda a, b: False, 
            cCS: Optional[Callable[[pd.DataFrame, list[Position]], bool]] = lambda a, b: False
        ):
        self.conditionToOpenLong = cOL
        self.conditionToCloseLong = cCL
        self.conditionToOpenShort = cOS
        self.conditionToCloseShort = cCS

    def check_condition(self, ind, positions: list[Position] = []):
        resp = []
        if self.conditionToOpenLong(ind, positions): resp.append('OPEN_LONG')
        if self.conditionToCloseLong(ind, positions): resp.append('CLOSE_LONG')
        if self.conditionToOpenShort(ind, positions): resp.append('OPEN_SHORT')
        if self.conditionToCloseShort(ind, positions): resp.append('CLOSE_SHORT')
        return resp
    

class RSI_Margins_Strategy(Strategy):


    def __init__(self, lowerMargin: float = 30, upperMargin: float = 70):
        
        super().__init__(
            cOL = lambda wrsi, na: (wrsi['Value'].iat[-1] <= lowerMargin) if not wrsi.empty else False, 
            cCL = lambda wrsi, na: (wrsi['Value'].iat[-1] >= upperMargin) if not wrsi.empty else False,
        )