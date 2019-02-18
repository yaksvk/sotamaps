#!/usr/bin/env python3
import os
import sys

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from flask import Flask

# add app dirs to sys paths


from sotamaps_app.app import app as sotamaps_application

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound(), {
    '/sotamaps': sotamaps_application
    })

if __name__ == '__main__':
    app.run(debug=True)
