import tkinter as tk
from tkinter import ttk

class InputPanel:
    def __init__(self, parent, generate_callback, risk_var):
        self.parent = parent
        self.generate_callback = generate_callback
        self.risk_var = risk_var
        self.selected_tickers = []
        
        title_frame = ttk.Frame(parent)
        title_frame.pack(side="top", fill="x", pady=(0, 5))
        
        self.title_label = ttk.Label(
            title_frame, 
            text="my portfolio", 
            font=("TkDefaultFont", 14, "bold")
        )
        self.title_label.pack(side="left", anchor="w")
        
        portfolio_section = ttk.Frame(parent, relief="groove", borderwidth=1)
        portfolio_section.pack(side="top", fill="x", padx=0, pady=(0, 15))
        
        portfolio_inner = ttk.Frame(portfolio_section, padding=10)
        portfolio_inner.pack(side="top", fill="x", expand=True)
        
        search_frame = ttk.Frame(portfolio_inner)
        search_frame.pack(side="top", fill="x", pady=(0, 12))
        
        search_container = ttk.Frame(search_frame, style="Search.TFrame")
        search_container.pack(side="top", fill="x")
        
        style = ttk.Style()
        style.configure("Search.TFrame", background="#f0f0f2", relief="flat", borderwidth=1)
        
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(
            search_container, 
            textvariable=self.entry_var, 
            width=25, 
            style="Search.TEntry"
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=5, padx=5)
        self.entry.bind("<Return>", lambda e: self.add_ticker())

        self.entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry.bind("<FocusOut>", self.on_entry_focus_out)

        search_icon = tk.Label(
            search_container, 
            text="🔍",
        )
        search_icon.pack(side="right", padx=(8, 10))
        
        style.configure("Search.TEntry", fieldbackground="#f0f0f2", borderwidth=0)
        
        ticker_container_frame = ttk.Frame(portfolio_inner)
        ticker_container_frame.pack(side="top", fill="x", pady=(0, 5))
        
        self.canvas = tk.Canvas(ticker_container_frame, height=65, highlightthickness=0, bg="#f5f5f7")
        self.canvas.pack(side="left", fill="x", expand=True)
        
        # don't pack scrollbar initially - will appear only when needed
        self.scrollbar = ttk.Scrollbar(ticker_container_frame, orient="vertical", command=self.canvas.yview)
        
        self.tokens_frame = tk.Frame(self.canvas, bg="#f5f5f7")
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.tokens_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.tokens_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.gen_button = ttk.Button(
            parent, 
            text="generate recommendations", 
            command=self.generate_callback
        )
        self.gen_button.pack(side="top", pady=(0, 10), fill="x")

        risk_section = ttk.Frame(parent)
        risk_section.pack(side="top", fill="x", pady=(5, 0))
        
        risk_title = ttk.Label(
            risk_section, 
            text="risk profile", 
            font=("TkDefaultFont", 14, "bold")
        )
        risk_title.pack(side="top", anchor="w", pady=(0, 8))
        
        risk_options = ttk.Frame(risk_section)
        risk_options.pack(side="top", fill="x", pady=(0, 5))
        
        high_risk = ttk.Radiobutton(
            risk_options, 
            text="high", 
            value="high-risk", 
            variable=self.risk_var,
            style="RiskOption.TRadiobutton"
        )
        high_risk.pack(side="top", anchor="w", pady=(0, 8))
        
        medium_risk = ttk.Radiobutton(
            risk_options, 
            text="medium", 
            value="medium-risk", 
            variable=self.risk_var,
            style="RiskOption.TRadiobutton"
        )
        medium_risk.pack(side="top", anchor="w", pady=(0, 8))
        
        low_risk = ttk.Radiobutton(
            risk_options, 
            text="low", 
            value="low-risk", 
            variable=self.risk_var,
            style="RiskOption.TRadiobutton"
        )
        low_risk.pack(side="top", anchor="w")

    def on_entry_focus_in(self, event):
        if self.entry_var.get() == "Enter ticker symbol and press Enter":
            self.entry_var.set("")

    def on_entry_focus_out(self, event):
        if not self.entry_var.get():
            self.entry_var.set("Enter ticker symbol and press Enter")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        if self.tokens_frame.winfo_height() > self.canvas.winfo_height():
            self.scrollbar.pack(side="right", fill="y")
        else:
            self.scrollbar.pack_forget()
    
    def on_canvas_configure(self, event):
        width = event.width
        self.canvas.itemconfig(self.canvas_window, width=width)
    
    def add_ticker(self):
        if self.entry_var.get() == "enter ticker symbol and press enter":
            return
            
        ticker = self.entry_var.get().strip().upper()
        if ticker and ticker not in self.selected_tickers:
            self.selected_tickers.append(ticker)
            self.entry_var.set("")
            self.refresh_tokens()
            self.entry.focus()

    def refresh_tokens(self):
        for widget in self.tokens_frame.winfo_children():
            widget.destroy()
            
        if not self.selected_tickers:
            empty_label = tk.Label(
                self.tokens_frame, 
                text="no tickers selected", 
                font=("TkDefaultFont", 10, "italic"),
                fg="#999999",
                bg="#f5f5f7"
            )
            empty_label.pack(pady=10)
            return
        
        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 300
        
        current_row = tk.Frame(self.tokens_frame, bg="#f5f5f7")
        current_row.pack(side="top", fill="x", pady=5)
        
        current_width = 0
        ticker_padding = 10
        
        for ticker in self.selected_tickers:
            ticker_frame = tk.Frame(
                current_row, 
                bg="#f0f0f2",
                padx=5,
                pady=2,
                relief="flat",
                bd=0
            )
            ticker_frame.pack(side="left", padx=(0, ticker_padding), pady=5)
            
            ticker_label = tk.Label(
                ticker_frame, 
                text=ticker,
                font=("TkDefaultFont", 11),
                fg="#333333",
                bg="#f0f0f2"
            )
            ticker_label.pack(side="left", padx=(2, 2))
            
            remove_btn = tk.Label(
                ticker_frame, 
                text="×",
                font=("TkDefaultFont", 11, "bold"),
                fg="#888888",
                cursor="hand2",
                bg="#f0f0f2"
            )
            remove_btn.pack(side="left", padx=(0, 2))
            remove_btn.bind("<Button-1>", lambda e, t=ticker: self.remove_ticker(t))
            
            ticker_frame.bind("<Enter>", lambda e, f=ticker_frame, l=ticker_label, b=remove_btn: 
                              self.on_ticker_hover(f, l, b, True))
            ticker_frame.bind("<Leave>", lambda e, f=ticker_frame, l=ticker_label, b=remove_btn: 
                              self.on_ticker_hover(f, l, b, False))
            
            ticker_width = len(ticker) * 9 + 25
            current_width += ticker_width + ticker_padding
            
            if current_width > canvas_width - 40 and ticker != self.selected_tickers[-1]:
                current_row = tk.Frame(self.tokens_frame, bg="#f5f5f7")
                current_row.pack(side="top", fill="x", pady=5)
                current_width = 0

    def on_ticker_hover(self, frame, label, btn, is_hover):
        if is_hover:
            frame.config(bg="#e6e6e9")
            label.config(bg="#e6e6e9")
            btn.config(bg="#e6e6e9", fg="#ff5555")
        else:
            frame.config(bg="#f0f0f2")
            label.config(bg="#f0f0f2")
            btn.config(bg="#f0f0f2", fg="#888888")

    def remove_ticker(self, ticker):
        if ticker in self.selected_tickers:
            self.selected_tickers.remove(ticker)
            self.refresh_tokens()

    def get_tickers(self):
        return self.selected_tickers