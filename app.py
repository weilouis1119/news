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
    img_path = 'templates/img/free.png'
    free_stream = return_img_stream(img_path)
    img_path = 'templates/img/chinatimes.png'
    china_stream = return_img_stream(img_path)
    img_path = 'templates/img/udn.jpeg'
    udn_stream = return_img_stream(img_path)
    img_path = 'templates/img/WordArt.png'
    logo_stream = return_img_stream(img_path) 
    return render_template('index.html',free_stream=free_stream,
                            china_stream=china_stream, udn_stream=udn_stream,
                            logo_stream=logo_stream, name="")


@app.route('/libertytimes')
def free():
    img_path = 'img/free.png'
    img_stream = return_img_stream(img_path)
    bar_path = 'img/free_bar.png'
    bar_stream = return_img_stream(bar_path)
    df = pd.read_csv('title_and_url/free.csv')[:50].to_dict('records')
    return render_template('index-1.html', img_stream=img_stream, bar_stream=bar_stream, news=df)

@app.route('/chinatimes')
def chinatimes():
    img_path = 'img/chinatimes.png'
    img_stream = return_img_stream(img_path)
    bar_path = 'img/chinatimes_bar.png'
    bar_stream = return_img_stream(bar_path)
    df = pd.read_csv('title_and_url/chinatimes.csv')[:50].to_dict('records')
    return render_template('index-2.html', img_stream=img_stream, bar_stream=bar_stream, news=df)

@app.route('/udn')
def udn():
    img_path = 'img/udn.png'
    img_stream = return_img_stream(img_path)
    bar_path = 'img/udn_bar.png'
    bar_stream = return_img_stream(bar_path)
    df = pd.read_csv('title_and_url/udn.csv')[:50].to_dict('records')
    return render_template('index-3.html', img_stream=img_stream, bar_stream=bar_stream,news=df)
@app.route('/about')
def about():
    return render_template('index-4.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
