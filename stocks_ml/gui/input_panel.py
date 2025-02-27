import tkinter as tk
from tkinter import ttk

class InputPanel:
    def __init__(self, parent, generate_callback):
        self.parent = parent
        self.generate_callback = generate_callback
        self.selected_tickers = []
        self.label = ttk.Label(parent, text="enter stock ticker:")
        self.label.pack(side="left")
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(parent, textvariable=self.entry_var, width=10)
        self.entry.pack(side="left", padx=5)
        self.add_button = ttk.Button(parent, text="add", command=self.add_ticker)
        self.add_button.pack(side="left")
        self.tokens_frame = ttk.Frame(parent)
        self.tokens_frame.pack(side="left", padx=10)
        self.gen_button = ttk.Button(parent, text="generate", command=self.generate_callback)
        self.gen_button.pack(side="left", padx=5)

    def add_ticker(self):
        ticker = self.entry_var.get().strip().upper()
        if ticker and ticker not in self.selected_tickers:
            self.selected_tickers.append(ticker)
            self.entry_var.set("")
            self.refresh_tokens()

    def refresh_tokens(self):
        for w in self.tokens_frame.winfo_children():
            w.destroy()
        for ticker in self.selected_tickers:
            f = ttk.Frame(self.tokens_frame, relief="ridge", borderwidth=1)
            f.pack(side="left", padx=2)
            l = ttk.Label(f, text=ticker)
            l.pack(side="left", padx=2)
            b = ttk.Button(f, text="x", command=lambda t=ticker: self.remove_ticker(t))
            b.pack(side="left", padx=2)

    def remove_ticker(self, ticker):
        if ticker in self.selected_tickers:
            self.selected_tickers.remove(ticker)
            self.refresh_tokens()

    def get_tickers(self):
        return self.selected_tickers
