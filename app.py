from flask import Flask
import os


app = Flask(__name__)


DATABASE_URI = os.getenv("DATABASE_URL", "test")

@app.route("/")
def root():
    return f"Hello from root\ndb_url: {DATABASE_URI}"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
