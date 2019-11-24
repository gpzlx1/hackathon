#coding:utf-8
import math
import re
import urllib
import requests
import os
import base64
from src import predict as pd
from src import train as ta
from src import buildnn

from io import BytesIO
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, make_response, json
from flask import send_file, flash

app = Flask(__name__, static_folder='static', template_folder='static', static_url_path='')
dataresource = ta.DataSource()

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    DownloadPath = 'model/' + filename
    return send_file(DownloadPath, as_attachment=True, attachment_filename=filename)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        bb64 = request.form["img_base64"]
        bb64 = bb64[bb64.find(',')+1:]
        with open('./pict/pre.png', 'wb') as f:
            f.write(base64.b64decode(bb64))
        result = pd.predict_with_load("./pict/pre.png")
        print(result)
        return jsonify(result)

@app.route('/')
def hello():
    return make_response(render_template('index.html', page='index.html'))
    
@app.route('/train', methods=["GET", "POST"])
def train():
    if request.method == "POST":
        os.system("rm -rf log/*")
        data = request.get_data()
        import json
        data = json.loads(data)
        status, cnn_or_err = buildnn.cnn(data)
        if(status):
            cnn = cnn_or_err
            #trainApp = ta.Train(dataresource)
            #trainApp.train(cnn)
            return jsonify({"status":True, "index":-1, "msg":"finish training"})
        else:
            err = cnn_or_err
            return jsonify(err)

if __name__ =="__main__":
    app.run(port='80', debug=False, host="0.0.0.0")



    
    





