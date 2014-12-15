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
                   "url": "http://yoogane.365lighthouse.net/reservation"
                  },
                  {"type": "view",
                   "name": unicode("订餐","utf-8").encode("utf-8"),
                   "url": "http://yoogane.365lighthouse.net/order"
                  },
                  {"type": "view",
                   "name": unicode("外卖","utf-8").encode("utf-8"),
                   "url": "http://yoogane.365lighthouse.net/takeout"
                  }
                  ]
          },
          {
          "type": "view",
          "name": unicode("会员","utf-8").encode("utf-8"),
          "url": "http://yoogane.365lighthouse.net/vip"
          },
          {
          "type": "view",
          "name": "About Us",
          "url": "http://yoogane.365lighthouse.net/about"
          }
         ]}

print payload
x = requests.post("https://api.weixin.qq.com/cgi-bin/menu/create?access_token=85gRr7xAWYIU4fNsivmHn_ZmlnnDeX8XjzBaAJ_gSDwzqQiFuwrB5XpgG2TMzGuhVWbwnX_UzarlKKbt_SYsYB9vqhIa1G4JXNRvoAtGPEE",data=json.dumps(payload,ensure_ascii=False))
print x.text
