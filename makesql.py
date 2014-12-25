#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from datetime import date
date = date.today()
print date

def makesql():  #初始化数据库
    con =MySQLdb.connect(host="localhost",user="root",passwd="root",\
            db="order_food",charset="utf8")
    cur = con.cursor()
    do = [cur,con]
    return do

def insert_seat(position_message):  #插入用户订座数据
    make,con = makesql()
    print position_message
    try:
        make.execute("insert into reservation (open_id,phone,user_name,come_date,come_time,come_people,position,other) values (%s,%s,%s,%s,%s,%s,%s,%s)",position_message)
        con.commit()
        return "OK"
    except Exception,e:
        return e
    make.close()
    con.close()

def insert_user(user_message):   #插入用户信息数据
    print user_message
    make,con = makesql()
    try:
        make.execute("insert into user (open_id,phone,user_name,vip) values (%s,%s,%s,%s)",user_message)
        con.commit()
        return "OK"
    except Exception,e:
        return e
    make.close()
    con.close()

def select_user(open_id):  #查询用户信息
    make,con = makesql()
    print open_id
    try:
        make.execute("select * from user where open_id=%s",open_id)
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
        make.execute("select phone,user_name,come_date,come_time,come_people,position,\
                other from reservation where review='pending' \
                and come_date=%s",date)
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()


def select_allowseat():  #查询已审核订座信息
    make,con = makesql()
    try:
        make.execute("select phone,user_name,come_date,come_time,come_people,position,\
                other from reservation where review='allow' and \
                come_date=%s",date)
        fetchall = make.fetchall()
        return fetchall
    except Exception,e:
        return e
    make.close()
    con.close()


def seat_allow(phone,date):  #审核通过订座
    make,con = makesql()
    try:
        result = make.execute("update reservation set review='allow' where \
                phone=%s and come_date=%s",(phone,date))
        con.commit()
        return result
    except Exception,e:
        return e
    make.close()
    con.close()

