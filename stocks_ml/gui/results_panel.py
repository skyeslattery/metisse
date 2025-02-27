import tkinter as tk
from tkinter import ttk

class ResultsPanel:
    def __init__(self, parent):
        self.parent = parent
        self.label = ttk.Label(parent, text="recommendations:")
        self.label.pack(side="top", anchor="w")
        self.listbox = tk.Listbox(parent, height=10)
        self.listbox.pack(side="top", fill="both", expand=True)

    def display_recommendations(self, recs):
        self.listbox.delete(0, tk.END)
        for ticker, score in recs:
            self.listbox.insert(tk.END, f"{ticker} - {score:.3f}")
