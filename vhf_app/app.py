#!/usr/bin/env python3
import os
import json
 
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from .vhf.adif import Adif
from .vhf.activity import Log

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            up_file = request.files['file']

            filename = secure_filename(up_file.filename)
            up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_adif',
                                    filename=filename, gridsquare=request.values.get('gridsquare', None)))
    return render_template('upload.html')

@app.route('/log/<filename>')
def uploaded_adif(filename):
   
    # gridsquare will be guessed from ADIF, if possible, but can be overridden
    log = Log(
        request.values.get('gridsquare', None), 
        os.path.join(app.config['UPLOAD_FOLDER'], filename)
    )
    
    # create json data for the map
    web = [{'call': qso.call, 'from': log.latlng, 'to': qso.latlng, 'gridsquare': qso.gridsquare} for qso in log.qsos]

    return render_template(
        'vhf_render.html', 
        log=log, 
        web=web,
        map_center=log.latlng
    )

if __name__ == '__main__':
    app.run(debug=True)
