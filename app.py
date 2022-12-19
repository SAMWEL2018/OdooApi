from threading import Thread
from time import sleep

from flask import Flask

from InvoiceProcessingService import InvoiceProcessingService

app = Flask(__name__)

pos = InvoiceProcessingService()


@app.route('/')
def server():
    return 'SERVER IS UP'


def fetch():
    while True:
        pos.processInvoice()
        sleep(3)


task = Thread(target=fetch(), daemon=False, name='background')
task.start()

if __name__ == '__main__':
    app.run()
