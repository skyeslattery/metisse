# Métissé - Stock Recommendation Engine

Analyze your stock portfolio and get recommendations for complementary investments to strengthen your overall investment strategy. Apply different risk profiles for more aggresive/conservative recommendations.

## Tech Stack

- **Backend**: Python, NumPy, yahoo_fin
- **Database**: SQLite (for data caching)
- **Frontend**: Tkinter

## Features

- Vector-based portfolio analysis with customizable risk tolerance parameters
- Feature extraction from financial time-series data using Yahoo Finance APIs
- Similarity scoring algorithm comparing stock vectors against portfolio vector
- Weighted recommendation system with risk-adjusted candidate filtering

## Installation/Usage

```bash
git clone https://github.com/skyeslattery/metisse.git
cd metisse

# Install dependencies
pip install -r requirements.txt

# Install Tkinter if needed (macOS)
brew install python-tk

# Run application
python -m metisse.main
```

Enter your stocks, select risk level, click generate. The app finds complementary investments based on your portfolio characteristics.
