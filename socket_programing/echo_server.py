# -*- coding: utf-8 -*- 
import sys
import socket

# 서버 socket 생성
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 주소, 포트 입력받아 bind
serv_addr = sys.argv[1]
serv_port = int(sys.argv[2])
serv.bind((serv_addr, serv_port))

# 서버 socket listen 함수 호출
serv.listen(1)

# 서버 socket이 받게 되는 data_sock과 clnt_addr 정보 수신 
data_sock, clnt_addr = serv.accept()

# 클라이언트가 '0'을 입력할 때까지 클라이언트가 입력한 메시지 조회 
while True:
    dnum = data_sock.recv(1)
    num = int.from_bytes(dnum, 'big')
    recv_buf = data_sock.recv(num)
    msg = recv_buf.decode()
    if msg == '0':
        break    
    print(f'received from client: {msg}')

    # 서버가 클라이언트에게 보낼 메시지
    send_buf = recv_buf
    num = len(send_buf)
    dnum = num.to_bytes(1, 'big')
    data_sock.send(dnum)
    data_sock.send(send_buf)

# 서버에 열려진 소켓 닫기
data_sock.close()
serv.close()



