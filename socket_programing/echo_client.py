
# -*- coding: utf-8 -*- port sys
import sys
import socket

# 클라이언트 socket 생성
clnt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 클라이언트가 연결될 주소와 포트 입력
clnt_addr = sys.argv[1]
clnt_port = int(sys.argv[2])
clnt.connect((clnt_addr, clnt_port))

# 클라이언트가 '0'을 입력할 때까지 서버에 메시지 전달
while True:
    msg = input('# ')
    send_buf = msg.encode()
    num = len(send_buf)
    bnum = num.to_bytes(1, 'big')
    clnt.send(bnum)
    clnt.send(send_buf)
    
    if msg == '0':
        break

    dnum = clnt.recv(1)
    num = int.from_bytes(dnum, 'big')

    recv_buf = clnt.recv(num)
    msg = recv_buf.decode()

    print(f'received : {msg}')  

# 클라이언트가 메시지 '0'을 입력하면 소켓 닫기
clnt.close()

