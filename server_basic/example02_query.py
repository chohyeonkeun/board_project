from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse  # 어떤 주소로 접속했는지 해석
# 해당파일 실행시킨 후, 127.0.0.1:8000 혹은 127.0.0.1:8000/?height=174&weight=70 접속
PORT = 8000

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200) # 이 페이지 접속하면 200으로 응답해라
        self.send_header('Content-type', 'text/html')  # 응답받은 페이지의 type 써줌
        self.end_headers()

        query_text = urlparse(self.path).query # urlparse가 url을 쪼개준다.(127.0.0.1:8000/?height=174&weight=70)
        print(query_text)  # querey_text = height=174&weight=70
        query_vars = parse_qs(query_text)
        print(query_vars)  # query_vars = {'height':['174'], 'weight':['70']}

        message = 'Welcome'
        form_html = """
            <form action='' method='post'>
                <label>Weight:<input type='text' name='weight'></label><br>
                <label>Height:<input type='text' name='height'></label><br>
                <input type='submit', value='Calc'>
            </form>
        """
        if 'weight' in query_vars and 'height' in query_vars:
            height = int(query_vars['height'][0])
            weight = int(query_vars['weight'][0])
            print(f'height: {height}, weight: {weight}')
            # query string으로 키와 몸무게를 전달받아서
            # bmi를 계산해서 message로 출력하시오
            bmi = str(round(weight / ((height/100) ** 2), 4))
            print('BMI :', bmi)
            message += ' BMI : ' + bmi

        message += form_html

        self.wfile.write(bytes(message, 'utf-8'))   # wfile : 파일처럼 보내준다.
        return

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length')) # 자료 몇바이트 보냈는지 확인
        print(self.headers)
        post_body = self.rfile.read(content_length)  # 길이만큼 받아온다, rfile : 파일을 받아온다.
        # post_body = b'weight=70&height=170'
        queries = parse_qs(post_body.decode('utf8'))   # 내용을 읽을 수 있다.
        # queries = {'weight : ['70'], 'height' : ['170']}
        message = "POST Test<br>Result]: " # 웹 브라우저에서 메시지 받아서 html로 보여준다.
        if 'weight' in queries and 'height' in queries:
            weight = int(queries['weight'][0])
            height = int(queries['height'][0])
            bmi = round(weight / ((height / 100) ** 2), 4)
            message += f'( Weight : {weight}, Height : {height}, BMI : {bmi} )'

        self.send_response(200) # 이 페이지 접속하면 200으로 응답해라
        self.send_header('Content-type', 'text/html')  # 응답받은 페이지의 type 써줌
        self.end_headers()

        self.wfile.write(bytes(message, 'utf-8')
        return


# 한 페이지에서 접속 Method에 따라 기능을 분기
# 회원 가입 페이지 domain.com/signup/
# Get : 회원가입 양식 보여주기
# Post : 전달받은 데이터를 처리해서 회원가입 진행하기(데이터베이스에 저장하기)

def run():
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, Handler)
    print('serving at PORT', PORT)
    httpd.serve_forever()

run()
