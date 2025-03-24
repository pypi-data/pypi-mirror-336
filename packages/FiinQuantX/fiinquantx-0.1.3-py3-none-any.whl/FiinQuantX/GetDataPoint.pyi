# This code is encrypted and does not contain viruses or Trojans.
from typing import Union

class GetDataPoint:
    def __init__(self, access_token: callable, 
                 ticker: str, 
                 field: str,
                 by: str, 
                 candle_index: int,
                 adjusted: Union[bool,None] = True) -> Union[float,int, str]:...






