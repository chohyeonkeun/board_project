import requests

from bs4 import BeautifulSoup

url = "https://www.naver.com/"

req = requests.get(url)
# print(req.status_code)
# print(type(req.status_code))
if req.status_code == requests.codes.ok:  # requests.codes.ok == 200 (하드코딩 피하기 위함)
    print("접속 성공")
    # 데이터 해석
    # print(req.text)
    html = BeautifulSoup(req.text, "html.parser")
    items = html.select('.ah_list .ah_item')
    for item in items:
        keyword = item.select_one('.ah_k')
        rank = item.select_one('.ah_r')
        # print(rank.attr['class'])
        # print(rank['class'])
        link = item.select_one('.ah_a')
        print(rank.text, keyword.text, link['href'])
    # for rank, keyword  in enumerate(keywords, 1):
    #     print(rank, keyword.text)
    # keywords = html.select('.ah_list .ah_k')
    # ranks = html.select('.ah_list .ah_r')
    # 어떤 요소를 찾고, 그 요소 안에 각각의 요소를 다시 찾을 수 있다.
    # span2 = html.select_one('span')


else:
    print("접속 실패")

