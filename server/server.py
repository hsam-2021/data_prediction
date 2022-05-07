import util
import sklearn
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)


@app.route('/get_job_names')
def get_job_names():
    response = jsonify({
        'job': util.get_job_names()
    })
    response.headers.add('')
    return "hello"


if __name__ == "__main__":
    print("Starting Flask server for customer subscription prediction...")
    app.run()
