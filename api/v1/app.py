#!/usr/bin/python3
"""Flask APplication"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """close storage"""
    storage.close()
    
    
@app.errorhandler(404)
def not_found(error):
    """Handles 404 Error"""
    return make_response(jsonify({'Error': 'Not Found'}), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)