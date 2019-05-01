import requests

from bs4 import BeautifulSoup

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%A1%9C%EB%98%90+%EB%8B%B9%EC%B2%A8%EB%B2%88%ED%98%B8&oquery=%EB%A1%9C%EB%98%90+%EB%B2%88%ED%98%B8&tqi=U7%2FFCdp0Jy0ssNWTEXKssssssll-475180"

custom_headers = {
    'referer' : 'https://www.naver.com',
    'user-agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
}

req = requests.get(url, headers = custom_headers)
# print(req.status_code)
# print(type(req.status_code))
if req.status_code == requests.codes.ok:  # requests.codes.ok == 200 (하드코딩 피하기 위함)
    print("접속 성공")
    # 데이터 해석
    # print(req.text)
    html = BeautifulSoup(req.text, "html.parser")

numbers = html.select('.num_box .num')
for number in numbers[:6]:
    print(number.text, end=", ")
print("보너스 번호 : ", numbers[-1].text)