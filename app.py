#! /usr/bin/python
#! -*- coding:utf-8 -*-
#! author: wickydong

import sys
from flask import Flask,render_template,request,redirect,url_for
import makesql
import requests
import json
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
        return render_template("order.html")
    order_list = request.form.getlist("dishes")
    return render_template("order_sure.html",order_list=order_list)

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
        if str(phone).isdigit() == True and len(str(phone)) == 11:
            seat_message = [open_id,phone,user_name,come_date,come_time,int(come_people), other]
            global access_token
            if user_status == "is":
                seat_insert = makesql.insert_seat(seat_message)
                print seat_insert
                if seat_insert == "OK":
                    put_msg = {"touser": open_id,
                               "msgtype": "text",
                               "text": {
                                    "content":"Your reservation is ok,Please wait a moment"
                                       }
                              }  
                    put = requests.post("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %access_token,data=json.dumps(put_msg))
                    print put.text
                    return "ok"
                return "wrong"
            else:
                user_message = [open_id,phone,user_name,vip]
                user_insert = makesql.insert_user(user_message)
                seat_insert = makesql.insert_seat(seat_message)
                print "user_insert:"+user_insert
                print "seat_insert:"+seat_insert
                if seat_insert == "OK" and user_insert == "OK":
                    put_msg = {"touser": open_id,
                               "msgtype": "text",
                               "text": {
                                    "content":"Your reservation is ok,Please wait a moment"
                                       }
                              }  
                    put = requests.post("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %access_token,data=json.dumps(put_msg))
                    print put.text
                    return "ok"
                return "wrong"
            #return render_template("choice_seat.html",open_id=open_id,\
             #      phone=phone,user_name=user_name,come_date=come_date,\
              #     come_time=come_time,come_people=come_people,other=other)
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

#@app.route("/reservation_sure",methods=["POST","GET"]) #确认订座
#def reservation_sure():
#    if request.method == "POST":              #此处需要加入接收用户wechatID进行判断或写入
#        open_id = request.form.get("open_id")
#        phone = request.form.get("phone")
#        user_name = request.form.get("user_name")
#        come_date = request.form.get("come_date")
#        come_time = request.form.get("come_time")
#        come_people = request.form.get("come_people")
#        other = request.form.get("other")
#        position = request.form.get("position")
#        vip = "NO"
#        seat_message = [open_id,phone,user_name,come_date,come_time,int(come_people),position, other]
#        user_message = [open_id,phone,user_name,vip]
#        seat_insert = makesql.insert_seat(seat_message)
#        user_insert =makesql.insert_user(user_message)
#        if seat_insert == "OK" and user_insert == "OK":
#            global access_token
#            put_msg = {"touser": open_id,
#                       "msgtype": "text",
#                       "text": {
#                                "content":"Your reservation is ok,Please wait a moment"
#                               }
#                      }
#            put = requests.post("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %access_token,data=json.dumps(put_msg))
#            print put.text
#            return "ok" 
#        return "wrong"
#    return "Please Use Post"

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

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/review_seat")   #后台显示订座信息
def review_seat():
    review_seat = makesql.select_seat()
    review_allowseat = makesql.select_allowseat()
    review_list = []
    allow_list = []
    if len(review_seat) != 0:
        for i in review_seat:
            phone = str(i[0])
            times = i[2].strftime("%Y-%m-%d")
            review_list.append((phone,i[1],times,i[3],i[4],i[5],i[6]))
    if len(review_allowseat) != 0:
        for i in review_allowseat:
            phone = str(i[0])
            times = i[2].strftime("%Y-%m-%d")
            allow_list.append((phone,i[1],times,i[3],i[4],i[5],i[6]))
    return render_template("review_seat.html",review_list=review_list,\
                allow_list=allow_list)

@app.route("/review_over")   #审核通过座位
def review_over():
    phone = request.args.get("phone")
    date = request.args.get("date")
    review_back = makesql.seat_allow(phone,date)
    return redirect(url_for("review_seat"))

@app.route("/review_change")  #审核修改座位
def review_change():
    pass


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
        print open_id
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
