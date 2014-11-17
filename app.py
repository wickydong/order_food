#! /usr/bin/python
#! -*- coding:utf-8 -*-

from flask import Flask,url_for,render_template,request
import MySQLdb

app = Flask(__name__)

@app.route("/")
def index():
    pass

@app.route("/order")
def order():
    pass

@app.route("/reservation")
def reservation():
    pass

@app.route("/vip")
def vip():
    pass

@app.route("/about")
def about():
    pass

if __name__ == "__main__":
    app.run()
