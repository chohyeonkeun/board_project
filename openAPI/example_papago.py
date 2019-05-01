import os
import sys
import urllib.request
import requests
import json

client_id = "WgUTvpW7bMXLBpZERraT"
client_secret = "2jEAq0evFb"

custom_header = {
    "X-Naver-Client-Id" : client_id,
    "X-Naver-Client-Secret" : client_secret,
}

encText = "안녕하세요."#input("번역할 문장을 입력하세요 : ")
# data = "source=ko&target=en&text=" + encText
data = {
    "source":"ko",
    "target":"en",
    "text":encText,
}

url = "https://openapi.naver.com/v1/papago/n2mt"
req = requests.post(url, headers=custom_header, data=data)

if req.status_code == requests.codes.ok:
    print("접속 성공")
    trans_data = json.loads(req.text)
    print(trans_data)
    print(trans_data['message']['result']['translatedText'])

