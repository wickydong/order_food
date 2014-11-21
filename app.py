#! /usr/bin/python
#! -*- coding:utf-8 -*-
#! author: wickydong

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
        print phone_number
        print other
        print come_date
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
