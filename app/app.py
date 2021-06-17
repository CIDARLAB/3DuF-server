"""
--------------------------------------------------------------------------------
Description:

Roadmap:

Written by W.R. Jackson <wrjackso@bu.edu>, DAMP Lab 2020
--------------------------------------------------------------------------------
"""
import sys

from flask import Flask

sys.path.append("/usr/lib/freecad-python3/lib")
import Draft
import FreeCAD
import Mesh
import Part

app = Flask(__name__)


@app.route("/echo/<input_string>")
def echo(input_string: str):
    return input_string


app.run(host="0.0.0.0", port=5000)
