from datetime import datetime

def timestamp():
    current_date = datetime.now()
    return current_date.strftime("%d/%m/%Y %H:%M")

def print_message(message:str):
    print(message)

def on_start():
    msg = f"Bot started at {timestamp()}"
    print_message(msg)

def on_shutdown():
    msg = f"Bot stopped at {timestamp()}"
    print_message(msg)

