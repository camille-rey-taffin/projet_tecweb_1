#! /usr/bin/env python
import threading
from backend import app as back_app
from frontend import app as front_app

def runBackend():
    back_app.run(host="localhost", port=5000, debug=False, threaded=True)

def runFrontend():
    front_app.run(host="localhost", port=8000, debug=False, threaded=True)

if __name__ == "__main__":
    t1 = threading.Thread(target = runBackend)
    t2 = threading.Thread(target = runFrontend)
    t1.start()
    t2.start()
