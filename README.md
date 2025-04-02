<p align="center">
  <img src="https://github.com/user-attachments/assets/7efe4dbb-338f-4716-bd37-591f6493385e" alt="logo" width="200"/>
</p>

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
brew install python-tk@3.11

# Run application
python -m metisse.main
```
**Note:** This application was designed with Tkinter 8.6. Using it with Python 3.13+ (Tkinter 9.0+) may result in visual differences due to rendering changes in newer Tkinter versions.

Enter your stocks, select risk level, click generate. The app finds complementary investments based on your portfolio characteristics.

## Screenshots
<img width="899" alt="results" src="https://github.com/user-attachments/assets/8a74fc9b-a387-423f-9f6d-9f26907f2abd" />
<img width="899" alt="generating" src="https://github.com/user-attachments/assets/12a195d8-8704-407f-8950-fa5d7b40ef8f" />

