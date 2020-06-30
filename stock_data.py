import yfinance as yf
from dataclasses import dataclass

@dataclass
class StockConfig:
    stock_name: str
    avg_short: int = 10
    avg_long: int = 50

class StockData:
    def __init__(self, config: StockConfig):
        self.data = yf.download(config.stock_name, period="3y", interval="1d", actions=True)
        # data = yf.download(ticker, period="6mo", interval="1d")

        self.closing = self.data.get("Close")
        self.avg_short = self.closing.rolling(window=config.avg_short).mean()
        self.avg_long = self.closing.rolling(window=config.avg_long).mean()
