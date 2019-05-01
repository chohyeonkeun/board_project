"""
메뉴 1 : 조회 급등 항목 10개의 현재가 출력


메뉴 2 : 1) 종목 코드를 입력받고 2) 해당 종목의 1페이지 주가 출력

메뉴 2-2 : 데이터 엑셀로 저장하기

1. 메뉴 구현하기
2. 1번 메뉴에 대한 크롤러
    2-1. 조회 급등 항목 10개 찾기
    2-2. 그 항목 1개에 대한 데이터 찾아서 출력
    2-3. 총 10개 항목에 대한 데이터 찾아서 출력
3. 2번 메뉴에 대한 크롤러
    3-1. 아무 항목이나 고정 - 1페이지 주가 출력
    3-2. 사용자에게 종목 코드 입력받아서 출력하기
"""

import requests
import json

def get_name(stock_code):
    url = "http://finance.daum.net/api/trend/market_capitalization?page=1&perPage=30&fieldName=marketCap&order=desc&market=KOSPI&pagination=true"
    custom_header = {
        'referer':"http://finance.daum.net/domestic",
        'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    }
    req = requests.get(url, headers=custom_header)
    if req.status_code == requests.codes.ok:
        cospy_data = json.loads(req.text)
        for i in range(len(cospy_data['data'])):
            if cospy_data['data'][i]['symbolCode'] == stock_code:
                corp_name = cospy_data['data'][i]['name']
                return corp_name
        return None
while True:
    try:
        stock_code = input('종목 코드를 입력하세요: ')
        url = "http://finance.daum.net/api/quote/"+stock_code+"/days?symbolCode="+stock_code+"&page=1&perPage=10&pagination=true"
        custom_header = {
            'referer' : "http://finance.daum.net/domestic",
            'user-agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        }
        req = requests.get(url, headers=custom_header)
        if req.status_code == requests.codes.ok:
            # print(req.text)
            current_price = json.loads(req.text)
            corp_name = get_name(stock_code)
            print(corp_name, current_price['data'][0]['tradePrice'])
        break
    except IndexError:
        print('코드를 다시 입력해주세요.')

