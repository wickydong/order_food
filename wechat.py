#! /usr/bin/python
# -*-coding:utf-8 -*-
# author: WickyDong
# mail: i@sihaizi.com
import requests
import json

payload = {
          "button": [
          {
          "name": unicode("预订","utf-8").encode("utf-8"),
          "sub_button": [
                 # {"type": "view",
                 #  "name": unicode("订座","utf-8").encode("utf-8"),
                 #  "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx51ae0018262ad036&redirect_uri=http%3a%2f%2fyoogane.sunzhongwei.com%2fwchat_sure%3faction%3dreservation&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                 # },
                  {"type": "view",
                   "name": unicode("订餐","utf-8").encode("utf-8"),
                   "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx51ae0018262ad036&redirect_uri=http%3a%2f%2fyoogane.sunzhongwei.com%2fwchat_sure%3faction%3dorder&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                  },
                  {"type": "view",
                   "name": unicode("外卖","utf-8").encode("utf-8"),
                   "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx51ae0018262ad036&redirect_uri=http%3a%2f%2fyoogane.sunzhongwei.com%2fwchat_sure%3faction%3dtakeout&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                  }
                  ]
          },
          {
          "type": "view",
          "name": unicode("Wifi","utf-8").encode("utf-8"),
          "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx51ae0018262ad036&redirect_uri=http%3a%2f%2fyoogane.sunzhongwei.com%2fwchat_sure%3faction%3dwifi&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
          },
          {
          "type": "view",
          "name": unicode("关于我们","utf-8").encode("utf-8"),
          "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx51ae0018262ad036&redirect_uri=http%3a%2f%2fyoogane.sunzhongwei.com%2fwchat_sure%3faction%3dabout&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
          }
         ]}

print payload
x = requests.post("https://api.weixin.qq.com/cgi-bin/menu/create?access_token=7Y3wC7_Mb8KCw8AXApQQpW_yMTSNxI5YGJd9_-u_9ThgchYnJPKjRXkJf6ckNUxa7P94Wi-B1_8DSoR7ttNtQv5-1h_lq4tBCPJwA1Yo9DQ",data=json.dumps(payload,ensure_ascii=False))
print x.text
