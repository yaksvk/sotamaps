#!/usr/bin/env python3
import os
 
from flask import Flask, request, redirect, url_for, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def vhf():
    return render_template('vhf.html')

if __name__ == '__main__':
    app.run(debug=True)
