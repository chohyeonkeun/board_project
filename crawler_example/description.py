"""
크롤러 : 웹 페이지에 있는 자료를 자동으로 수집하는 프로그램
ex) 검색엔진
--->
Robot.txt : 검색엔진에게 어디까지 검색을 허용할 것이냐?

브라우저가 혹은 크롤러가 어떤 식으로 서버에 접근해서 데이터를 가져가느냐?
1. 주소를 입력하면 해당 서버로 접근한다.
2. 웹 서버 프로그램이 해당 주소에 맞는 내용을 전달한다.

requests (urllib의 wrapper클래스)

3. 받은 내용을 해석해서 화면에 보여준다.
3-1. 받은 내용을 해석해서 내가 원하는 데이터를 찾는다. 뽑아낸다.
BeautifulSoup
+ HTML 코드의 해석
+ CSS Selector 만드는 방법

모듈 설치
1. requests
2. BeautifulSoup4

"""
import json
import requests
from bs4 import BeautifulSoup
url = "http://finance.daum.net/api/quote/A048410/days?symbolCode=A048410&page=2&perPage=100&pagination=true"

customer_header = {
    'referer': 'http://finance.daum.net/quotes/A048410#current/quote',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}

req = requests.get(url, headers = customer_header)
print(req.text)
if req.status_code == requests.codes.ok:
    print('접속 성공')
    stock_data = json.loads(req.text)
    for daily_data in stock_data['data'][:5]:
        print(daily_data['date'], daily_data['tradePrice'])