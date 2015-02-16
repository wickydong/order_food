#! /usr/bin/python
#! -*- coding:utf-8 -*-
#! author: wickydong

import sys
from flask import Flask,render_template,request,redirect,url_for
import makesql
import requests
import json
import base64
reload(sys)
sys.setdefaultencoding("utf-8")
app = Flask(__name__)

reservation_data = {"appid": "wx51ae0018262ad036",
              "redirect_uri": "http%3a%2f%2fyoogane.sunzhongwei.com%2freservation",
              "response_type": "code",
              "scope": "snsapi_base#wechat_redirect"
             }

# ---------------------------------------- #
#               #用戶管理#                 #
# ---------------------------------------- #

@app.route("/takeout")   #外卖
def takeout():
    if request.method == "POST":
        open_id = request.form.get("open_id")
        phone = request.form.get("phone_number",default="")
        user_name = request.form.get("user_name",default="")
        come_date = request.form.get("come_date",default="")
        come_time = request.form.get("come_time",default="")
        come_people = request.form.get("come_people",default="")
        other = request.form.get("other")
        return render_template("choice_seat.html",open_id=open_id,\
               phone=phone,user_name=user_name,come_date=come_date,\
               come_time=come_time,come_people=come_people,other=other)
    open_id = request.args.get("open_id")
    select_user = makesql.select_user(open_id)
    if len(select_user) == 0:
        return "您还没有成为会员"
    phone = str(select_user[0][2])
    user_name = str(select_user[0][3])
    return str(open_id + " " + phone)

@app.route("/order",methods=["GET","POST"])   #订餐页
def order():
    if request.method == "GET":
        open_id = request.args.get("open_id")
        come_from = request.args.get("come_from")
        return render_template("order.html",open_id=open_id)
    order_list = str(request.form.getlist("dishes")[0]).split(",")
    open_id = request.form.get("open_id")
    a = 0
    order = []
    food_list = []
    for i in order_list:
        i = str(i).strip("[").strip("\"").strip("]")
        a += 1
        if a < 3:
            food_list.append(i)
        elif a == 3:
            food_list.append(i)
            order.append(food_list)
            food_list = []
            a = 0
    money = 0            
    for o in order:
        money = int(o[0]) * float(o[2]) + money
    print money
    return "ok"

@app.route("/reservation",methods=["POST","GET"])  #订座
def reservation():
    if request.method == "POST":
        open_id = request.form.get("open_id")
        phone = request.form.get("phone_number",default="")
        user_name = request.form.get("user_name",default="")
        come_date = request.form.get("come_date",default="")
        come_time = request.form.get("come_time",default="")
        come_people = request.form.get("come_people",default="")
        other = request.form.get("other")
        user_status = request.form.get("user_status")
        vip = "NO"
    #return render_template("reservation.html",open_id='1231231',user_status='is',phone='13012345678')
        if str(phone).isdigit() == True and len(str(phone)) == 11:
            seat_message = [open_id,come_date,come_time,int(come_people), other]
            global access_token
            if user_status == "is":
                seat_insert = makesql.insert_seat(seat_message)
                if type(seat_insert) == int and seat_insert > 0:
                    put_msg = {"touser": open_id,
                               "msgtype": "text",
                               "text": {
                                    "content":"Your reservation is ok,Please wait a moment"
                                       }
                              }  
                    put = requests.post("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %access_token,data=json.dumps(put_msg))
                    base_msg = open_id + "|" + str(seat_insert)
                    base_64 =  base64.encodestring(base_msg)
                    return base_64
                return "wrong"
            else:
                user_message = [open_id,phone,user_name,vip]
                user_insert = makesql.insert_user(user_message)
                seat_insert = makesql.insert_seat(seat_message)
                if seat_insert > 0  and user_insert > 0:
                    put_msg = {"touser": open_id,
                               "msgtype": "text",
                               "text": {
                                    "content":"Your reservation is ok,Please wait a moment"
                                       }
                              }  
                    put = requests.post("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %access_token,data=json.dumps(put_msg))
                    base_msg = open_id + "|" + str(seat_insert)
                    base_64 =  base64.encodestring(base_msg)
                    return base_64
                return "wrong"
        select_user = makesql.select_user(open_id)
        if len(select_user) == 0:
            return render_template("reservation.html",open_id=open_id,user_status="notis")
        phone = str(select_user[0][2])
        user_name = str(select_user[0][3])
        return render_template("reservation.html",open_id=open_id,phone=phone,user_name=user_name,user_status="is")
    open_id = request.args.get("open_id")
    select_user = makesql.select_user(open_id)
    if len(select_user) == 0:
        return render_template("reservation.html",open_id=open_id,user_status="notis")
    phone = str(select_user[0][2])
    user_name = str(select_user[0][3])
    return render_template("reservation.html",open_id=open_id,phone=phone,user_name=user_name,user_status="is")


@app.route("/vip",methods=["GET","POST"])    #会员
def vip():
    if request.method == "POST":
        open_id = request.form.get("open_id")
        phone = request.form.get("phone_number",default="")
        user_name = request.form.get("user_name",default="")
        come_date = request.form.get("come_date",default="")
        come_time = request.form.get("come_time",default="")
        come_people = request.form.get("come_people",default="")
        other = request.form.get("other")
        return render_template("choice_seat.html",open_id=open_id,\
               phone=phone,user_name=user_name,come_date=come_date,\
               come_time=come_time,come_people=come_people,other=other)
    open_id = request.args.get("open_id")
    select_user = makesql.select_user(open_id)
    if len(select_user) == 0:
        return "您还没有成为会员"
    phone = str(select_user[0][2])
    user_name = str(select_user[0][3])
    return str(open_id + " " + phone)

@app.route("/about")  #关于
def about():
    pass

# ---------------------------------------- #
#                #后台管理#                #
# ---------------------------------------- #
@app.route("/getfood")
def getfood():
    food_list = json.dumps(makesql.show_food())
    return food_list
@app.route("/admin",methods=["POST","GET"])
def admin():
    if request.method == "GET": 
        return render_template("admin.html")
    modify_type = request.form["modify_type"]
    if modify_type == "add_food":
        return render_template("add_food.html") 
    if modify_type == "modify_food":
        show_food = makesql.show_food()
        return render_template("modify_food.html",show_food=show_food) 
    if modify_type == "del_food":
        return render_template("del_food.html") 

@app.route("/review_seat")   #后台显示订座信息
def review_seat():
    review_seat = makesql.select_seat()
    review_allowseat = makesql.select_allowseat()
    review_list = []
    allow_list = []
    if len(review_seat) != 0:
        for i in review_seat:
            open_id = i[0]
            date = i[1]
            time = i[2]
            come = i[3]
            other = i[4]
            user_sel = makesql.select_user(open_id)
            phone = user_sel[0][2]
            name = user_sel[0][3]
            review_list.append((phone,name,date,time,come,other,open_id))
    if len(review_allowseat) != 0:
        for i in review_allowseat:
            open_id = i[0]
            date = i[1]
            time = i[2]
            come = i[3]
            other = i[4]
            user_sel = makesql.select_user(open_id)
            phone = user_sel[0][2]
            name = user_sel[0][3]
            allow_list.append((phone,name,date,time,come,other,open_id))
    return render_template("review_seat.html",review_list=review_list,\
                allow_list=allow_list)

@app.route("/review_over")   #审核通过座位
def review_over():
    open_id = request.args.get("open_id")
    date = request.args.get("date")
    review_back = makesql.seat_allow(open_id,date)
    print review_back
    return redirect("http://yoogane.sunzhongwei.com/review_seat")
@app.route("/review_change")  #审核修改座位
def review_change():
    pass

@app.route("/modify_food")
def modify_food():
    modify_status = request.args.get("modify_status")
    img_url = request.args.get("img_url")
    food_name = request.args.get("food_name")
    price = request.args.get("price")
    food_msg = (img_url,food_name,price)
    choice_food = request.args.get("choice_food")
    if modify_status == "add_food":
        add_food = makesql.add_food(food_msg)
        if add_food == "OK":
            return "菜品已添加成功"
        return "菜品添加失败...ORZ"
    if modify_status == "modify_food":
        modify_food = makesql.modify_food(food_msg)
        if modify_food == "OK":
            return "菜品已修改成功"
        return "菜品修改失败...ORZ"
    if modify_status == "del_food":
        del_food = makesql.del_food(food_msg)
        if del_food == "OK":
            return "菜品已删除成功"
        return "菜品删除失败...ORZ"
    if modify_status == "choice_food":
        showline_food = makesql.showline_food(choice_food)
        imgurl = showline_food[0][0]
        price = showline_food[0][1]
        return render_template("choice_food.html",choice_food=choice_food,imgurl=imgurl,price=price)


# ---------------------------------------- #
#               #WECHAT相关#               #
# ---------------------------------------- #


@app.route("/wchat_sure",methods=["GET","POST"])  #WECHAT开发者验证
def wechat_sure():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")
    #body = request.data
    code = request.args.get("code")
    state = request.args.get("state")
    action = request.args.get("action")
    if echostr:
        return echostr
    if code:
        payload = {"appid": "wx51ae0018262ad036",
                   "secret": "de8a8682f69e79cd20ceea978831eb7b",
                   "code": code,
                   "grant_type": "authorization_code"}
        get_token = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token",params=payload)
        open_id =  str(json.loads(get_token.text)["openid"])
        #print type(action)
        if str(action) == "reservation":
            return redirect("http://yoogane.sunzhongwei.com/reservation?open_id=%s" % open_id)
        if str(action) == "vip":
            return redirect("http://yoogane.sunzhongwei.com/vip?open_id=%s" % open_id)
        if str(action) == "takeout":
            return redirect("http://yoogane.sunzhongwei.com/takeout?open_id=%s" % open_id)
        if str(action) == "order":
            return redirect("http://yoogane.sunzhongwei.com/order?open_id=%s" % open_id)
        if str(action) == "about":
            return redirect("http://yoogane.sunzhongwei.com/about?open_id=%s" % open_id)
    else:
        print request.data
        return request.data

access_token = ""
@app.route("/access_token")
def access_token():
    global access_token
    access_token = request.args.get("access_token")
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
