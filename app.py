#!/usr/bin/env python3
import os
 
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from sotamaps import sotamaps

app = Flask(__name__)

@app.route('/<int:callsign>')
@app.route('/')
def map(callsign=None):
    return render_template('map_osm.html',callsign=callsign)

# json services
@app.route('/json/summits/<int:callsign>')
@app.route('/json/summits')
def json_summits(callsign=None):
    
    # only for testing
    #response = [
    #    {"SummitCode": "SP/BZ-001", "Latitude": "49.5792", "Longitude": "19.5292"}
    #]

    response = sotamaps.summits_for_callsign(callsign)
    return jsonify(response) 

@app.route('/test')
def debug_url():
    #return sotamaps.get_uniques_for_id(45)
    return ','.join(sotamaps.get_uniques_for_id(45))

#@app.route('/vhf')
#def vhf_app(adif_file=None):
#    return vhf

if __name__ == '__main__':
    app.run(debug=True)
