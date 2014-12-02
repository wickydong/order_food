#! /usr/bin/python
#! -*- coding:utf-8 -*-
#! author: wickydong

import sys
from flask import Flask,url_for,render_template,request
import makesql
#con =MySQLdb.connect(host="localhost",user="root",passwd="root",db="order_food")
#cur = con.cursor()
reload(sys)
sys.setdefaultencoding("utf-8")
app = Flask(__name__)

@app.route("/")   #首页
def index():
    return render_template("index.html")

@app.route("/takeout")   #外卖
def takeout():
    pass

@app.route("/order",methods=["GET","POST"])   #订餐页
def order():
    if request.method == "GET":
        return render_template("order.html")
    order_list = request.form.getlist("dishes")
    return render_template("order_sure.html",order_list=order_list)

@app.route("/reservation",methods=["POST","GET"])  #订座
def reservation():
    if request.method == "POST":
        phone = request.form.get("phone_number",default="")
        user_name = request.form.get("user_name",default="")
        come_datetime = request.form.get("come_datetime",default="")
        come_people = request.form.get("come_people",default="")
        other = request.form.get("other")
        return render_template("choice_seat.html",\
               phone=phone,user_name=user_name,come_datetime=come_datetime,\
               come_people=come_people,other=other)
    return render_template("reservation.html")

@app.route("/reservation_sure",methods=["POST","GET"]) #确认订座
def reservation_sure():
    if request.method == "POST":
        phone = request.form.get("phone")
        user_name = request.form.get("user_name")
        come_datetime = request.form.get("come_datetime")
        come_people = request.form.get("come_people")
        other = request.form.get("other")
        position = request.form.get("position")
        vip = "NO"
        seat_message = [phone,user_name,come_datetime,int(come_people),position,\
                other]
        user_message = [phone,user_name,vip]
        seat_insert = makesql.insert_seat(seat_message)
        user_insert =makesql.insert_user(user_message)
        if seat_insert == "OK" and user_insert == "OK":
            #return render_template("position.html")
            return "ok"
        print seat_insert,user_insert
        return "wrong"
    return "Please Use Post"

@app.route("/vip")    #会员
def vip():
    pass

@app.route("/about")  #关于
def about():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
