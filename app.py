from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np
import matplotlib.pyplot as plt
import cv2
import base64
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({"data": "testing"})

if __name__ == '__main__':
    app.run(debug=True)
