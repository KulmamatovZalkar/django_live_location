import os
import threading
import subprocess
from tracker.bot import run_bot

def run_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    subprocess.run(['daphne', '-p', '8000', 'myproject.asgi:application'])

if __name__ == '__main__':
    threading.Thread(target=run_django).start()
    run_bot()


#7471557412:AAFVvom3aSU4GnFJg7L6fxhLheOO-ZOv97g