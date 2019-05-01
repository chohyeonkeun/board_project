#1. HTTP Response만 하는 서버
import http.server
import socketserver

PORT = 8000 # 서버에 접속하는 포트

# 요청이 들어오면 어느 객체가 요청을 해석하고 처리할 것이냐?
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at PORT", PORT)
    httpd.serve_forever()

