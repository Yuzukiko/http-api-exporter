from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Info
import threading
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

#load env
load_dotenv()
api_list = json.loads(os.getenv("API_LIST"))
debug_mode = os.getenv("DEBUG")

# add all additional metrics
def setup(api_list):
    for entry in api_list:
        print(f"entry -> {entry}")
        threading.Thread(target=checker_thread, daemon=True, kwargs={"name":entry["name"], "description":entry["description"], "url":entry["url"], "request_interval":entry["request_interval"]}).start()

# checker thread thats sends request every x seconds
def checker_thread(name, description, url, request_interval):
    last_request = ""
    api_info = Info(name, description)
    while True:
        current_request = requests.get(url).json()
        if last_request != current_request:
            last_request = current_request
        api_info.info(last_request)
        time.sleep(request_interval)
        
# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    setup(api_list)
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)