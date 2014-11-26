#! /usr/bin/python
#! -*- coding:utf-8 -*-
#! author: wickydong

from flask import Flask,url_for,render_template,request
import MySQLdb

app = Flask(__name__)

@app.route("/")   #首页
def index():
    return render_template("index.html")

@app.route("/takeout")   #外卖
def takeout():
    pass

@app.route("/order")   #订餐页
def order():
    return render_template("order.html")

@app.route("/order_sure",methods=["POST"])  #订餐确认页
def order_sure():
    order_list = request.form.getlist("dishes")
    return render_template("order_sure.html",order_list=order_list)

@app.route("/reservation",methods=["POST","GET"])  #订座
def reservation():
    if request.method == "POST":
        phone_number = request.form.get("phone_number",default="")
        user_name = request.form.get("user_name",default="")
        come_date = request.form.get("come_date",default="")
        come_time = request.form.get("come_time",default="")
        come_people = request.form.get("come_people",default="")
        room_type = request.form.get("room_people",default="")
        other = request.form.get("other")
        return phone_number
    return render_template("reservation.html")
@app.route("/vip")    #会员
def vip():
    pass

@app.route("/about")  #关于
def about():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
