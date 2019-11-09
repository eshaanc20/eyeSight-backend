from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
import base64
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        colorRanges = {
            'Orange': ([6,150,150], [22,255,255]),
            'Red': ([170, 40, 40], [180,255,255]),
            'Gold': ([[22,40,40]], [24,255,255]),
            'Yellow': ([24,40,40],[35,255,255]),
            'Green' : ([32,40,40], [85,255,255]),
            'Teal': ([94,40,40], [98, 255,255]),
            'Blue': ([98,40,40],[115,255,255]),
            'Purple': ([127, 40, 40], [138, 255, 255]),
            'Pink': ([160, 40, 40], [170, 255, 255]),
            'Brown': ([6, 100, 100], [20, 170, 170]),
            'Gray': ([110, 0, 0], [120, 180, 180]),
            'White': ([0, 0, 200], [255, 255, 255]),
            'Black': ([0, 0, 0], [255, 120, 120]),
            'Cyan': ([84, 40, 40], [92, 255, 255])
        }

        base_64 = request.json["base_64"]
        image = Image.open(BytesIO(base64.b64decode(base_64)))
        image.save("image.png")

        #Converts image from BGR to RGB
        BGRimage = cv2.imread("image.png")
        os.remove("image.png")
        HSVimage = cv2.cvtColor(BGRimage, cv2.COLOR_BGR2HSV)

        #dictionary to count number of undetected pixels in image for each color
        pixelDict = {}

        for color in colorRanges:
            lowerLimit = np.array(colorRanges[color][0])
            upperLimit = np.array(colorRanges[color][1])
            imageSize = np.shape(HSVimage)
            background = np.zeros((imageSize[1], imageSize[2]))
            mask = cv2.inRange(HSVimage, lowerLimit, upperLimit)
            detection = cv2.bitwise_and(HSVimage, HSVimage, mask=mask)
            pixelCount = 0
            for pixel in detection:
                if pixel.any() != background.any():
                    pixelCount += 1
                    pixelDict[color] = pixelCount

        #List of most dominant colors in the image
        color = []
        maxKey = max(pixelDict, key = pixelDict.get)
        for key in pixelDict:
            if pixelDict[key] == pixelDict[maxKey]:
                color.append(key)
        return jsonify({'answer': color, 'data': pixelDict})
    elif request.method == 'GET':
        return jsonify({'Project': 'eyeSight-backend'})
    else:
        return("")

if __name__ == '__main__':
    app.run(debug=True)
