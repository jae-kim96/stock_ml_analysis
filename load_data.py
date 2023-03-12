from util import load_symbols_csv_to_db, load_stock_price_to_db, load_etf_price_to_db
from DB import DB

DATABASE = DB('stock_data.db')

def load_symbols_data():
    ## Loading the Symbols File into DB
    load_symbols_csv_to_db(DATABASE.connection)
    
    
def load_stock_data():
    ## Loading the Stock Price Data into the DB
    load_stock_price_to_db(DATABASE.connection)

def load_etf_data():
    ## Loading the ETF Price Data into the DB
    load_etf_price_to_db(DATABASE.connection)

if __name__ == '__main__':
    load_symbols_data()
    load_stock_data()
    load_etf_data()