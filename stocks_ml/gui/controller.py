import tkinter as tk
from tkinter import ttk
import threading

from stocks_ml.data.api import get_ticker_data
from stocks_ml.data.models import recommend_stocks_by_gap
from stocks_ml.data.processing import (
    compute_features_from_data,
    feature_vector_from_features,
    compute_portfolio_vector
)
from stocks_ml.config.candidates import CANDIDATE_TICKERS
from .input_panel import InputPanel
from .results_panel import ResultsPanel

class AppController:
    def __init__(self, root):
        self.root = root
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(side="top", fill="x")
        bottom_frame = ttk.Frame(root, padding=10)
        bottom_frame.pack(side="top", fill="both", expand=True)

        self.input_panel = InputPanel(top_frame, self.on_generate)
        self.results_panel = ResultsPanel(bottom_frame)

    def on_generate(self):
        t = threading.Thread(target=self.run_flow)
        t.start()

    def build_candidate_vectors(self, exclude=None):
        exclude = exclude or []
        vectors = {}
        for c in CANDIDATE_TICKERS:
            if c in exclude:
                continue
            try:
                ticker_obj, df = get_ticker_data(c, data_type="historical")
                feats = compute_features_from_data(ticker_obj, df)
                vec = feature_vector_from_features(feats)
                vectors[c] = vec
            except Exception as e:
                print(f"error processing candidate {c}: {e}")
        return vectors

    def run_flow(self):
        tickers = self.input_panel.get_tickers()
        if not tickers:
            self.update_results([("no tickers entered", 0.0)])
            return

        feature_vectors = []
        for ticker in tickers:
            try:
                ticker_obj, df = get_ticker_data(ticker, data_type="historical")
                feats = compute_features_from_data(ticker_obj, df)
                vec = feature_vector_from_features(feats)
                feature_vectors.append(vec)
            except Exception as e:
                print(f"error fetching {ticker}: {e}")
        if not feature_vectors:
            self.update_results([("no valid data", 0.0)])
            return

        portfolio_vec = compute_portfolio_vector(feature_vectors)
        candidate_vecs = self.build_candidate_vectors(exclude=tickers)
        if not candidate_vecs:
            self.update_results([("no candidate data", 0.0)])
            return

        recs = recommend_stocks_by_gap(portfolio_vec, candidate_vecs, 'medium-risk', top_n=5)
        self.update_results(recs)

    def update_results(self, recs):
        self.root.after(0, lambda: self.results_panel.display_recommendations(recs))
