from stocks_ml.data.db import create_table
from stocks_ml.gui.app import run_app
from stocks_ml.data.loader import load_candidates

if __name__ == "__main__":
    load_candidates()
    create_table()
    run_app()