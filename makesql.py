#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from datetime import date
date = date.today()

def makesql():  #初始化数据库
    con =MySQLdb.connect(host="localhost",user="root",passwd="root",\
            db="order_food",charset="utf8")
    con.autocommit(True)
    cur = con.cursor()
    do = [cur,con]
    return do

def insert_seat(position_message):  #插入用户订座数据
    make,con = makesql()
    print position_message
    try:
        make.execute("insert into reservation (open_id,come_date,come_time,come_people,other) values (%s,%s,%s,%s,%s)",position_message)
        insert_id = int(con.insert_id())
        con.commit()
        return insert_id
    except Exception,e:
        return e
    make.close()
    con.close()

def insert_food(food_msg):
    make,con = makesql()
    try:
        make.execute("insert into reservation (open_id,money,food) values(%s,%s,%s)",food_msg)
        insert_id = int(con.insert_id())
        con.commit()
        return insert_id
    except Exception,e:
        return 3
    make.close()
    con.close()
def insert_user(user_message):   #插入用户信息数据
    print user_message
    make,con = makesql()
    try:
        make.execute("insert into user (open_id,phone,user_name,vip) values (%s,%s,%s,%s)",user_message)
        insert_id = int(con.insert_id())
        con.commit()
        return insert_id
    except Exception,e:
        return e
    make.close()
    con.close()

def select_user(open_id):  #查询用户信息
    make,con = makesql()
    try:
        make.execute("select * from user where open_id=%s",open_id)
        con.commit()
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        print e
        return e
    make.close()
    con.close()


def select_seat():  #查询订座信息
    make,con = makesql()
    try:
        make.execute("select open_id,date_format(come_date,'%%Y-%%m-%%d'),come_time,come_people,\
                other from reservation where review='pending'\
                and date_format(come_date,'%%Y-%%m-%%d')=%s",date)
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()


def reservation_show(open_id,seat_id):  #展示给用户的订座信息
    make,con = makesql()
    try:
        make.execute("select date_format(come_date,'%%Y-%%m-%%d'),come_time,come_people,\
                other from reservation where open_id='%s' and id='%s'" %(open_id,seat_id))
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()


def select_allowseat():  #查询已审核订座信息
    make,con = makesql()
    try:
        make.execute("select open_id,date_format(come_date,'%%Y-%%m-%%d'),come_time,come_people,\
                other from reservation where review='allow' and \
                date_format(come_date,'%%Y-%%m-%%d')=%s",date)
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()


def seat_allow(open_id,date):  #审核通过订座
    make,con = makesql()
    print open_id
    try:
        result = make.execute("update reservation set review='allow' where \
                open_id='%s' and date_format(come_date,'%%Y-%%m-%%d')='%s'" %(open_id,date))
        con.commit()
        return result
    except Exception,e:
        return e
    make.close()
    con.close()

def add_food(food_msg):  #修改菜品信息（供后台使用）
    make,con = makesql()
    try:
        make.execute("insert into food (img_url,food_name,price) values (%s,%s,%s)",food_msg)
        con.commit()
        return "OK"
    except Exception,e:
        return e
    make.close()
    con.close()


def modify_food(food_msg):  #修改菜品信息（供后台使用）
    make,con = makesql()
    img_url = food_msg[0]
    food_name = food_msg[2]
    price = food_msg[1]
    print img_url,food_name,price
    try:
        a = make.execute("update food set img_url='%s',price='%s' where food_name='%s'" %(img_url,price,food_name))
        print a
        con.commit()
        return "OK"
    except Exception,e:
        return e
    make.close()
    con.close()


def del_food(food_msg):  #删除菜品信息（供后台使用）
    make,con = makesql()
    img_url = food_msg[0]
    food_name = food_msg[2]
    price = food_msg[1]
    try:
        a = make.execute("delete from food where food_name='%s'" % food_name)
        con.commit()
        return "OK"
    except Exception,e:
        return e
    make.close()
    con.close()

def show_food():  #展示菜品信息（供后台使用）
    make,con = makesql()
    try:
        make.execute("select img_url,food_name,price from food")
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()
def showline_food(food_name):  #展菜品信息（供后台使用）
    make,con = makesql()
    try:
        make.execute("select img_url,price from food where food_name=%s",food_name)
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()

def user_info():
    make,con = makesql()
    try:
        make.execute("select username,passwd from user_info")
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()
