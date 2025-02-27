import sqlite3
import json
from stocks_ml.config.settings import DB_PATH

def create_connection(db_file: str = DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(db_file)

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            data TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_stock_data(symbol: str, data: dict):
    conn = create_connection()
    cursor = conn.cursor()
    json_data = json.dumps(data)
    cursor.execute('''
        INSERT INTO stocks (symbol, data)
        VALUES (?, ?)
        ON CONFLICT(symbol) DO UPDATE SET data = excluded.data, last_updated = CURRENT_TIMESTAMP
    ''', (symbol, json_data))
    conn.commit()
    conn.close()

def get_stock_data(symbol: str) -> dict:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM stocks WHERE symbol = ?', (symbol,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

if __name__ == '__main__':
    create_table()
    dummy_data = {"test": "value"}
    insert_stock_data("IBM", dummy_data)
    data = get_stock_data("IBM")
    print(data)
