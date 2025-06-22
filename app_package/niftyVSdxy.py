import yfinance as yf
import pandas as pd
import datetime as dt


class historical_data:
    def __init__(self, ticker, start_date="2020-01-01", end_date=dt.datetime.now(), interval="1d",ma_len=44):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.ma_len=ma_len

    def load_data(self):
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date, interval=self.interval, progress=False)
        df.columns=[i for i,_ in df.columns]
        if df.empty:
            print(f"No data for {self.ticker}")
            return pd.DataFrame()

        df[f"{self.ma_len}_DMA"] = df["Close"].rolling(window=self.ma_len).mean()
        df.dropna(inplace=True)
        return df


if __name__=="__main__":
    nifty_index = historical_data("^NSEI")
    dollar_index = historical_data("DX-Y.NYB")
    print(nifty_index.load_data())

