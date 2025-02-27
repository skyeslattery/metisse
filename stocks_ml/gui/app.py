import tkinter as tk
from stocks_ml.data.db import create_table
from .controller import AppController

def run_app():
    create_table()
    root = tk.Tk()
    root.title("ml stock recommender")
    root.geometry("800x600")
    AppController(root)
    root.mainloop()
