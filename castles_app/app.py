#!/usr/bin/env python3
import os

from flask import Flask, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def map():
    return render_template('map_osm.html')

if __name__ == '__main__':
    app.run(debug=True)
