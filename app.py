from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Histogram, make_wsgi_app
from prometheus_client import Info
import threading
import time
import requests
import logging
from dotenv import load_dotenv
import os
import sys
import json

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

#load env
load_dotenv()
api_list = json.loads(os.getenv("API_LIST"))
debug_mode = (os.getenv('DEBUG', 'False') == 'True')
port = int(os.getenv('PORT', 5000))

# add all additional metrics
def setup(api_list):
    for entry in api_list:
        print(f"Running checker thread for {entry}")
        threading.Thread(target=checker_thread, daemon=True, kwargs={"name":entry["name"], "description":entry["description"], "url":entry["url"], "request_interval":entry["request_interval"]}).start()

# checker thread thats sends request every x seconds
def checker_thread(name, description, url, request_interval):
    api_info = Info(name, description)
    while True:
        app.logger.info(f"{name} - Checking request response")
        current_request = requests.get(url).json()
        app.logger.info(f"{name} - Updating response to {current_request}")
        api_info._value.update({"value": json.dumps(current_request)})
        time.sleep(request_interval)
        
# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    setup(api_list)
    app.run(host="0.0.0.0", port=port, debug=debug_mode)