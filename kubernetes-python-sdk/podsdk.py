import psutil
from flask import Flask
from kubernetes import client, config
import os

cpu = psutil.cpu_percent()

if cpu > 5:
    print("Cpu is greater than 5")
    app = Flask(__name__)
    @app.route("/")
    def hello():
         return "Hello from Python!"
    if __name__ == "__main__":
        app.run(host='0.0.0.0')


