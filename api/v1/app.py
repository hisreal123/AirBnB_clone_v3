#!/usr/bin/python3
"""
Flask app for AirBnB
"""

from flask import Flask
from api.v1.views import app_views
from models import storage
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

# 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
