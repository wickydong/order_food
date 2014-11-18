#! /usr/bin/python
#! -*- coding:utf-8 -*-

from flask import Flask,url_for,render_template,request
import MySQLdb

app = Flask(__name__)

@app.route("/")   #首页
def index():
    pass

@app.route("/takeout")   #外卖
def takeout():
    pass

@app.route("/order")   #订餐
def order():
    pass

@app.route("/reservation")  #订座
def reservation():
    pass

@app.route("/vip")    #会员
def vip():
    pass

@app.route("/about")  #关于
def about():
    pass

if __name__ == "__main__":
    app.run()
