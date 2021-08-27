#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 09:20:08 2021

@author: louis
"""
from flask import Flask, render_template,request
import pandas as pd


def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

app = Flask(__name__)

@app.route("/")
def index():
    if request.method=='POST':
        if request.values['send']=='送出':
            return render_template('index.html',name=request.values['user'])
    return render_template('index.html',name="")


@app.route('/libertytimes')
def free():
    img_path = 'free.png'
    img_stream = return_img_stream(img_path)
    df = pd.read_csv('free.csv')[:20].to_dict('records')
    return render_template('index-1.html', img_stream=img_stream, news=df)

@app.route('/chinatimes')
def chinatimes():
    img_path = 'chinatimes.png'
    img_stream = return_img_stream(img_path)
    df = pd.read_csv('chinatimes.csv')[:20].to_dict('records')
    return render_template('index-2.html', img_stream=img_stream, news=df)

@app.route('/udn')
def udn():
    img_path = 'udn.png'
    img_stream = return_img_stream(img_path)
    df = pd.read_csv('udn.csv')[:20].to_dict('records')
    return render_template('index-3.html', img_stream=img_stream,news=df)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
