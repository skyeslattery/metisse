import tkinter as tk
from tkinter import ttk

class ResultsPanel:
    def __init__(self, parent):
        self.parent = parent
        
        title_frame = ttk.Frame(parent)
        title_frame.pack(side="top", fill="x", pady=(0, 15))
        
        self.title_label = ttk.Label(
            title_frame, 
            text="Results", 
            font=("TkDefaultFont", 16, "bold")
        )
        self.title_label.pack(side="left", anchor="w")
        
        self.results_frame = ttk.Frame(parent)
        self.results_frame.pack(side="top", fill="both", expand=True)
        
        self.initial_frame = ttk.Frame(self.results_frame)
        self.initial_frame.pack(fill="both", expand=True)
        
        initial_content = ttk.Frame(self.initial_frame)
        initial_content.place(relx=0.5, rely=0.5, anchor="center")
        
        empty_title = ttk.Label(
            initial_content,
            text="No Results Yet",
            font=("TkDefaultFont", 14, "bold")
        )
        empty_title.pack(pady=(0, 5))
        
        self.description = ttk.Label(
            initial_content,
            text="Enter stock tickers and select risk profile, then click Generate to see recommendations.",
            wraplength=300,
            justify="center"
        )
        self.description.pack(pady=5)
    
    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def display_recommendations(self, recs):
        self.clear_results()
        
        if not recs:
            no_results = ttk.Label(
                self.results_frame,
                text="No recommendations found",
                font=("TkDefaultFont", 12)
            )
            no_results.pack(pady=20)
            return
        
        rec_title = ttk.Label(
            self.results_frame,
            text="Recommended Stocks",
            font=("TkDefaultFont", 14, "bold")
        )
        rec_title.pack(side="top", anchor="w", pady=(0, 15))
            
        header_frame = ttk.Frame(self.results_frame)
        header_frame.pack(side="top", fill="x", pady=(0, 5))
        
        ticker_header = ttk.Label(
            header_frame, 
            text="TICKER", 
            font=("TkDefaultFont", 12, "bold")
        )
        ticker_header.pack(side="left", padx=(10, 40))
        
        score_header = ttk.Label(
            header_frame, 
            text="SCORE", 
            font=("TkDefaultFont", 12, "bold")
        )
        score_header.pack(side="left")
        
        separator = ttk.Separator(self.results_frame, orient="horizontal")
        separator.pack(fill="x", pady=5)

        results_list = ttk.Frame(self.results_frame)
        results_list.pack(side="top", fill="both", expand=True)
        
        for i, (ticker, score) in enumerate(recs):
            row_frame = ttk.Frame(results_list, padding=(5, 8))
            row_frame.pack(side="top", fill="x", pady=2)
            
            if i % 2 == 0:
                row_frame.configure(style="EvenRow.TFrame")
            
            # Ticker label
            ticker_label = ttk.Label(
                row_frame, 
                text=ticker, 
                font=("TkDefaultFont", 12)
            )
            ticker_label.pack(side="left", padx=(10, 40))
            
            score_formatted = f"{score:.3f}" if isinstance(score, float) else score
            score_label = ttk.Label(
                row_frame, 
                text=score_formatted, 
                font=("TkDefaultFont", 12)
            )
            score_label.pack(side="left")