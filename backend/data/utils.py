from datetime import datetime

def format_currency(value, symbol='$'):
    return f"{symbol}{value:,.2f}"

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
