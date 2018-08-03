#!/usr/bin/env python3
import os
 
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from sotamaps import sotamaps

app = Flask(__name__)

@app.route('/')
def map():
    return render_template('map.html')

# json services
@app.route('/json/summits')
def json_summits():
    response = [
        {"SummitCode": "SP/BZ-001", "Latitude": "49.5792", "Longitude": "19.5292"}
    ]

    response = sotamaps.test()
    return jsonify(response) 

@app.route('/test')
def debug_url():
    #return sotamaps.get_uniques_for_id(45)
    return ','.join(sotamaps.get_uniques_for_id(45))

if __name__ == '__main__':
    app.run(debug=True)
