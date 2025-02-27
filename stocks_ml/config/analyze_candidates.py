import pandas as pd
import numpy as np
import yfinance as yf
from stocks_ml.config.candidates import CANDIDATE_TICKERS
from stocks_ml.data.db import get_stock_data
from stocks_ml.data.processing import compute_features_from_data, feature_vector_from_features
from stocks_ml.data.loader import load_candidates
# helper file to find the ideal feature vector


def compute_candidate_feature_vectors():
    candidate_feature_vectors = []
    for ticker in CANDIDATE_TICKERS:
        data = get_stock_data(ticker)
        
        history_json = data.get("history")
        df = pd.read_json(history_json)
        
        ticker_obj = yf.Ticker(ticker)
        try:
            features = compute_features_from_data(ticker_obj, df)
            vector = feature_vector_from_features(features)
            candidate_feature_vectors.append(vector)
        except Exception as e:
            print(f"error computing features: {e}")
    return candidate_feature_vectors

def compute_ideal_from_benchmarks(feature_vectors: list) -> np.ndarray:
    return np.median(np.array(feature_vectors), axis=0)

if __name__ == '__main__':
    load_candidates()
    candidate_vectors = compute_candidate_feature_vectors()
    
    ideal_vector = compute_ideal_from_benchmarks(candidate_vectors)
    print(ideal_vector)
