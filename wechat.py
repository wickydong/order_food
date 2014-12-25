#! /usr/bin/python
# -*-coding:utf-8 -*-
import requests
import json

payload = {
          "button": [
          {
          "name": unicode("预订","utf-8").encode("utf-8"),
          "sub_button": [
                  {"type": "view",
                   "name": unicode("订座","utf-8").encode("utf-8"),
                   "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx51ae0018262ad036&redirect_uri=http%3a%2f%2fyoogane.sunzhongwei.com%2fwchat_sure%3faction%3dreservation&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                  },
                  {"type": "view",
                   "name": unicode("订餐","utf-8").encode("utf-8"),
                   "url": "http://yoogane.sunzhongwei.com/order"
                  },
                  {"type": "view",
                   "name": unicode("外卖","utf-8").encode("utf-8"),
                   "url": "http://yoogane.sunzhongwei.com/takeout"
                  }
                  ]
          },
          {
          "type": "view",
          "name": unicode("会员","utf-8").encode("utf-8"),
          "url": "http://yoogane.sunzhongwei.com/vip"
          },
          {
          "type": "view",
          "name": "About Us",
          "url": "http://yoogane.sunzhongwei.com/about"
          }
         ]}

print payload
x = requests.post("https://api.weixin.qq.com/cgi-bin/menu/create?access_token=TH3TyF7leAbrfo29OjSUUXCgVrUmvACF8yddsM8AV6fDRgYXOvgZBmgDxc3b5HfzBFZVRuW5crJQJaQ4vgco6HVwwizis3P6v0LJliQp9Pk",data=json.dumps(payload,ensure_ascii=False))
print x.text
