import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database.db")
