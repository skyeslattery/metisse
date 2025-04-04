import tkinter as tk
from metisse.data.db import create_table
from .controller import AppController

def run_app():
    create_table()
    root = tk.Tk()
    root.title("métissé")
    root.geometry("900x450")
    root.configure(bg="#f5f5f7")
    
    # minsize 80% original
    root.minsize(720, 360)
    root.maxsize(1170, 470)
    
    AppController(root)

    center_window(root)
    root.mainloop()
    
def center_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 900) // 2
    y = (screen_height - 450) // 2
    
    root.geometry(f"+{x}+{y}")