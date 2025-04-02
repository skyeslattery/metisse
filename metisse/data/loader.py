from metisse.config.candidates import CANDIDATE_TICKERS
from metisse.data.api import get_ticker_data
from metisse.data.db import get_stock_data, insert_stock_data

def load_candidates():
    for ticker in CANDIDATE_TICKERS:
        cached = get_stock_data(ticker)
        if not cached:
            try:
                data = get_ticker_data(ticker, 'historical', serialize=True)
                print(f"loaded data for {ticker}")
                insert_stock_data(ticker, data)
            except Exception as e:
                print(f"error loading data for {ticker}: {e}")
        else:
            print(f"data already cached for {ticker}")

