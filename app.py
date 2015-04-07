#! /usr/bin/python
#! -*- coding:utf-8 -*-
#! author: wickydong

import sys
from flask import Flask,render_template,request,redirect,url_for,session
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

@app.route("/takeout",methods=["POST"])   #外卖
def takeout():
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
    food = ""       
    for o in order:
        money = int(o[0]) * float(o[2]) + money
        food = food + o[1] + "|"
    food_msg = (open_id,money,food)
    insert_id = makesql.insert_takeout(food_msg)
    if type(insert_id) == int and insert_id > 0:
        base_msg = open_id + "|" + str(insert_id)
        base_64 = base64.encodestring(base_msg)
        print base_msg,base_64
        return base_64
    return insert_id


@app.route("/takeout_user",methods=["POST","GET"])  #外卖信息
def takeout_user():
    if request.method == "POST":
        base_64 = request.form.get("base_64")
        phone = request.form.get("phone_number",default="")
        user_name = request.form.get("user_name",default="")
        come_date = request.form.get("come_date",default="")
        come_time = request.form.get("come_time",default="")
        other = request.form.get("other")
        user_status = request.form.get("user_status")
        vip = "NO"
        base_64 = base64.decodestring(base_64).split("|")
        open_id = base_64[0]
        takeout_id = base_64[1]
        if str(phone).isdigit() == True and len(str(phone)) == 11:
            takeout_message = [come_date,come_time,other,open_id,takeout_id]
            print takeout_message
            global access_token
            if user_status == "is":
                takeout_update = makesql.update_takeout(takeout_message)
                if takeout_update == "ok":
                    put_msg = {"touser": open_id,
                               "msgtype": "text",
                               "text": {
                                    "content":"Your reservation is ok,Please wait a moment"
                                       }
                              }  
                    put = requests.post("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %access_token,data=json.dumps(put_msg))
                    return base_64
                print takeout_update
                return "wrong"
            else:
                user_message = [open_id,phone,user_name,vip]
                user_insert = makesql.insert_user(user_message)
                takeout_update = makesql.update_takeout(takeout_message)
                if takeout_update == "ok"  and user_insert > 0:
                    put_msg = {"touser": open_id,
                               "msgtype": "text",
                               "text": {
                                    "content":"Your reservation is ok,Please wait a moment"
                                       }
                              }  
                    put = requests.post("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %access_token,data=json.dumps(put_msg))
                    return base_64
                return "wrong"
    base_64 = request.args.get("base_64")
    base_64 = base64.decodestring(base_64).split("|")
    open_id = base_64[0]
    select_user = makesql.select_user(open_id)
    if len(select_user) == 0:
        return render_template("takeout_user.html",open_id=open_id,user_status="notis",base_64=base_64)
    phone = str(select_user[0][2])
    user_name = str(select_user[0][3])
    return render_template("takeout_user.html",phone=phone,user_name=user_name,user_status="is",base_64=base_64)

@app.route("/order",methods=["GET"])   #订餐页
def order():
    open_id = request.args.get("open_id")
    c_from = request.args.get("c_from")
    if c_from == "order" or c_from == "takeout":
        return render_template("order.html",open_id=open_id,c_from=c_from)
    else:
        return "宝贝，不要胡闹"

@app.route("/order_food",methods=["POST"])
def order_food():
    order_list = str(request.form.getlist("dishes")[0]).split(",")
    open_id = request.form.get("open_id")
    if order_list != None and open_id != None:
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
        food = ""       
        for o in order:
            money = int(o[0]) * float(o[2]) + money
            food = food + o[1] + "|"
        food_msg = (open_id,money,food)
        insert_id = makesql.insert_food(food_msg)
        if type(insert_id) == int and insert_id > 0:
            base_msg = open_id + "|" + str(insert_id)
            base_64 = base64.encodestring(base_msg)
            print base_64
            return base_64
        return insert_id 
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
            seat_message = [open_id,come_date,come_time,int(come_people), other]
            print seat_message
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
                print seat_insert
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
    base_64 = request.args.get("base_64")
    base_64 = base64.decodestring(base_64).split("|")
    open_id = base_64[0]
    select_user = makesql.select_user(open_id)
    if len(select_user) == 0:
        return render_template("reservation.html",open_id=open_id,user_status="notis")
    phone = str(select_user[0][2])
    user_name = str(select_user[0][3])
    return render_template("reservation.html",open_id=open_id,phone=phone,user_name=user_name,user_status="is")
'''
    open_id = request.args.get("open_id")
    select_user = makesql.select_user(open_id)
    if len(select_user) == 0:
        return render_template("reservation.html",open_id=open_id,user_status="notis")
    phone = str(select_user[0][2])
    user_name = str(select_user[0][3])
    return render_template("reservation.html",open_id=open_id,phone=phone,user_name=user_name,user_status="is")
'''

@app.route("/reservation_sure/<base_msg>")
def reservation_sure(base_msg=None):
    if base_msg == None:
        return "Your Request Method Is Wrong, Please Go Away."
    base_64 = base64.decodestring(base_msg).split("|")
    open_id = base_64[0]
    seat_id = base_64[1]
    print seat_id
    seat_msg = makesql.reservation_show(open_id,seat_id)
    return render_template("reservation_sure.html",base_64=base_msg,seat_msg=seat_msg)

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

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method =="POST":
        username = request.form["user_name"]
        passwd = request.form["passwd"]
        user_info = makesql.user_info()[0]
        if username == str(user_info[0]) and passwd == str(user_info[1]):
            session['username'] = username
            return redirect("http://yoogane.sunzhongwei.com/admin")
        return "User or PassWord is Wrong"
    return '''
        <form action="" method="post">
            <p><input type="text" name="user_name">
            <p><input type="password" name="passwd">
            <p><input type=submit value=Login>
        </form>
    '''
@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect("http://yoogane.sunzhongwei.com/login")
            
@app.route("/admin",methods=["POST","GET"])
def admin():
    if request.method == "GET" and 'username' in session: 
        return render_template("admin.html")
    if 'username' in session and request.method == "POST":
        modify_type = request.form["modify_type"]
        if modify_type == "add":
            return render_template("modify_food.html",status="add") 
        if modify_type == "modify":
            show_food = makesql.show_food()
            return render_template("modify_food.html",status="modify",show_food=show_food) 
        if modify_type == "del":
            show_food = makesql.show_food()
            return render_template("modify_food.html",status="del",show_food=show_food) 
    return redirect("http://yoogane.sunzhongwei.com/login")

@app.route("/modify_food",methods=["POST","GET"])
def modify_food():
    if request.method == "POST" and 'username' in session:
        modify_status = request.form.get("modify_status")
        img_url = request.form.get("img_url")
        food_name = request.form.get("food_name")
        price = request.form.get("price")
        food_msg = (img_url,food_name,price)
        choice_food = request.form.get("choice_food")
        if modify_status == "add":
            add_food = makesql.add_food(food_msg)
            if add_food == "OK":
                return "菜品已添加成功"
            return "菜品添加失败...ORZ"
        if modify_status == "modify":
            modify_food = makesql.modify_food(food_msg)
            if modify_food == "OK":
                return "菜品已修改成功"
            return "菜品修改失败...ORZ"
        if modify_status == "del":
            showline_food = makesql.showline_food(choice_food)
            food_msg = (showline_food[0][0],showline_food[0][1],choice_food)
            del_food = makesql.del_food(food_msg)
            if del_food == "OK":
                return "菜品已删除成功"
            return "菜品删除失败...ORZ"
    return "You are wrong"
@app.route("/review_seat")   #后台显示订座信息
def review_seat():
    if 'username' in session:
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
    return "貌似姿势不对"

@app.route("/review_over")   #审核通过座位
def review_over():
    if 'username' in session:
        open_id = request.args.get("open_id")
        date = request.args.get("date")
        review_back = makesql.seat_allow(open_id,date)
        print review_back
        return redirect("http://yoogane.sunzhongwei.com/review_seat")
    return "貌似姿势不对"
@app.route("/review_change")  #审核修改座位
def review_change():
    pass


#@app.route("/select_user")
#def select_user():
#    open_id = request.args.get("open_id")
#    user_msg = makesql.select_user(open_id)
#    if len(user_msg) != 0:
#        phone = user_msg[0][2]
#        user_name = user_msg[0][3]
#        return phone + "|" + user_name
#    else:
#        return None


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
            return redirect("http://yoogane.sunzhongwei.com/order?open_id=%s&c_from=takeout" % open_id)
        if str(action) == "order":
            return redirect("http://yoogane.sunzhongwei.com/order?open_id=%s&c_from=order" % open_id)
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

app.secret_key = "\x11\x93}\xdd\xb1\xdd\x19\x88s\xde\x13\n9t\x12\x07\xfe\xf3*\xf7\xe1\x0fVj"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
