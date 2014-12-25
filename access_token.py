#! /usr/bin/python
# -*-coding: utf-8 -*-
import time
import requests
import json
while True:
    payload = {"appid": "wx51ae0018262ad036",
               "secret": "de8a8682f69e79cd20ceea978831eb7b",
               "grant_type": "client_credential"}
    request_access_token = requests.get("https://api.weixin.qq.com/cgi-bin/token",params=payload)
    access_token =  str(json.loads(request_access_token.text)["access_token"])
    token_msg = {"access_token": access_token}
    request_order = requests.get("http://0.0.0.0:5000/access_token",params=token_msg)
    time.sleep(7100)
