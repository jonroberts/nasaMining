#!./venv/bin/python

from flask import Flask

# creates the app instance using the name of the module
app = Flask(__name__)

print __name__, " app created." # to remove later

