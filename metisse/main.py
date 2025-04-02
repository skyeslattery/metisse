from metisse.data.db import create_table
from metisse.gui.app import run_app
from metisse.data.loader import load_candidates

if __name__ == "__main__":
    load_candidates()
    create_table()
    run_app()