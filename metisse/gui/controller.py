import tkinter as tk
from tkinter import ttk
import threading
from tkinter import font as tkfont

from metisse.data.api import get_ticker_data
from metisse.data.models import recommend_stocks_by_gap
from metisse.data.processing import (
    compute_features_from_data,
    feature_vector_from_features,
    compute_portfolio_vector
)
from metisse.config.candidates import CANDIDATE_TICKERS
from .input_panel import InputPanel
from .results_panel import ResultsPanel
from PIL import Image, ImageTk

class AppController:
    def __init__(self, root):
        self.root = root
        
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=11)
        
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        style.configure("TButton", padding=6, relief="flat", background="#4a7dfc", foreground="white")
        style.map("TButton", background=[('active', '#3a6de6')])
        style.configure("TFrame", background="#f5f5f7")
        style.configure("TLabel", background="#f5f5f7")
        style.configure("EvenRow.TFrame", background="#f0f0f2")
        style.configure("RiskOption.TRadiobutton", background="#f5f5f7")
        style.map("RiskOption.TRadiobutton", background=[('active', '#f0f0f2')])
        
        style.configure("Bordered.TFrame", background="#f5f5f7", relief="groove", borderwidth=2)
        
        header_frame = ttk.Frame(root, padding=5)
        header_frame.pack(fill="x", pady=(5, 0))
        
        img = Image.open("metisse/assets/metisse_logo.png")
        img = img.resize((70, 20), Image.Resampling.LANCZOS)

        logo_img = ImageTk.PhotoImage(img)
        logo_label = ttk.Label(header_frame, image=logo_img)
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=(20, 10))
        
        main_container = ttk.Frame(root, padding=0)
        main_container.pack(fill="both", expand=True, padx=20, pady=5)

        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=2)

        left_frame = ttk.Frame(main_container, padding=15, style="Bordered.TFrame", width=300, height=500)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_frame.grid_propagate(False)

        right_frame = ttk.Frame(main_container, padding=15, style="Bordered.TFrame", height=500)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        self.risk_var = tk.StringVar(value="medium-risk")
        
        self.input_panel = InputPanel(left_frame, self.on_generate, self.risk_var)
        self.results_panel = ResultsPanel(right_frame)

        # for loading animation
        self.dot_count = 0
        self.loading_active = False
        self.progress_count = 0
        self.total_steps = 100

    def on_generate(self):
        self.results_panel.clear_results()
        self.results_panel.show_loading()
        self.loading_active = True
        self.progress_count = 0
        
        # start animation loop
        self.animate_loading()
        
        # start processing thread
        t = threading.Thread(target=self.run_flow)
        t.start()
    
    def animate_loading(self):
        if self.loading_active:
            self.dot_count = (self.dot_count + 1) % 4
            self.results_panel.update_loading_dots(self.dot_count, None, self.progress_count, len(CANDIDATE_TICKERS))
            self.root.after(500, self.animate_loading)

    def update_progress(self, increment=1):
        self.progress_count = min(self.progress_count + increment, 100)

    def build_candidate_vectors(self, exclude=None):
        exclude = exclude or []
        vectors = {}
        progress_count = 0
        total_count = len([c for c in CANDIDATE_TICKERS if c not in exclude])
        
        for c in CANDIDATE_TICKERS:
            if c in exclude:
                continue
                    
            self.progress_count += 1
                
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
            self.update_results([("please enter stock tickers to analyze", 0.0)])
            return

        print(f"analyzing your portfolio: {', '.join(tickers)}")
        
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
            self.update_results([("could not retrieve valid data for your tickers", 0.0)])
            return

        portfolio_vec = compute_portfolio_vector(feature_vectors)
        
        candidate_vecs = self.build_candidate_vectors(exclude=tickers)
        
        if not candidate_vecs:
            self.update_results([("no candidate data available", 0.0)])
            return

        risk_profile = self.risk_var.get()
        
        print("computing recommendations...")
        recs = recommend_stocks_by_gap(portfolio_vec, candidate_vecs, risk_profile, top_n=5)

        self.loading_active = False
        self.update_results(recs)

    def update_results(self, recs):
        self.root.after(0, lambda: self.results_panel.display_recommendations(recs))