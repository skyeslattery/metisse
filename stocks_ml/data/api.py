import yfinance as yf

def get_ticker_data(symbol: str, data_type: str = "historical", serialize: bool = False):
    ticker_obj = yf.Ticker(symbol)
    if data_type == "intraday":
        df = ticker_obj.history(period="1d", interval="5m", auto_adjust=False)
    elif data_type == "historical":
        df = ticker_obj.history(period="1mo", interval="1d", auto_adjust=False)
    else:
        raise ValueError("data_type must be either 'intraday' or 'historical'")
    if df.empty:
        raise Exception(f"no data returned for {symbol}")
    if serialize:
        return {"info": ticker_obj.info, "history": df.to_json()}
    return ticker_obj, df

if __name__ == '__main__':
    try:
        ticker_obj, df = get_ticker_data("MSFT", data_type="historical")
        print("ticker info:")
        print(ticker_obj.info)
        print("historical data:")
        print(df.head())
    except Exception as e:
        print(e)
