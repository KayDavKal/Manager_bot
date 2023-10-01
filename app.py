from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0')

def stay_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    stay_alive()
