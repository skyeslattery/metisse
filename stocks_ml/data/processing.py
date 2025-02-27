import numpy as np

def compute_features_from_data(ticker_obj, df) -> dict:
    if df.empty:
        raise ValueError("no historical data available")
    prices = df["Close"].values
    volumes = df["Volume"].values
    avg_price = np.mean(prices)
    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns) if returns.size > 0 else 0.0
    avg_volume = np.mean(volumes)
    
    features = {
        "avg_price": avg_price,
        "volatility": volatility,
        "avg_volume": avg_volume,
    }
    
    info = ticker_obj.info
    features["trailingPE"] = info.get("trailingPE", 0) or 0
    features["forwardPE"] = info.get("forwardPE", 0) or 0
    features["marketCap"] = info.get("marketCap", 0) or 0
    features["dividendYield"] = info.get("dividendYield", 0) or 0
    features["beta"] = info.get("beta", 0) or 0
    features["priceToBook"] = info.get("priceToBook", 0) or 0
    features["profitMargins"] = info.get("profitMargins", 0) or 0
    return features

def feature_vector_from_features(features: dict) -> np.ndarray:
    return np.array([
        features["avg_price"],
        features["volatility"],
        features["avg_volume"],
        features["trailingPE"],
        features["forwardPE"],
        features["marketCap"],
        features["dividendYield"],
        features["beta"],
        features["priceToBook"],
        features["profitMargins"]
    ])

def compute_portfolio_vector(feature_vectors: list) -> np.ndarray:
    if not feature_vectors:
        raise ValueError("no feature vectors provided")
    return np.mean(feature_vectors, axis=0)

if __name__ == '__main__':
    from stocks_ml.data.api import get_ticker_data
    try:
        ticker_obj, df = get_ticker_data("MSFT", data_type="historical")
        feats = compute_features_from_data(ticker_obj, df)
        vector = feature_vector_from_features(feats)
        print("Computed Features:")
        print(feats)
        print("Feature Vector:")
        print(vector)
    except Exception as e:
        print("Error:", e)
