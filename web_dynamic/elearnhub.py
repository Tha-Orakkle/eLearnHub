#!/usr/bin/python3
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """removes current session"""
    storage.close()


@app.route('/elearn', methods=['GET'], strict_slashes=False)
def elearn():
    """ElearnHub Home"""
    return render_template('home.html')
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)