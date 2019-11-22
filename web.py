#coding:utf-8
import math
import re
import urllib
import requests
import os
import base64
from src import predict as pd


from io import BytesIO
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, make_response, json
from flask import send_file, flash
from werkzeug import secure_filename
app = Flask(__name__, static_folder='static')

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    DownloadPath = 'model/' + filename
    return send_file(DownloadPath, as_attachment=True, attachment_filename=filename)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        bb64 = request.form["img_base64"]
        bb64 = bb64[bb64.find(',')+1:]
        with open('./pict/pre.jpg', 'wb') as f:
            f.write(base64.b64decode(bb64))
        result = pd.predict_with_load("./pict/pre.jpg")
        print(result)
        return jsonify(result)

    
    





