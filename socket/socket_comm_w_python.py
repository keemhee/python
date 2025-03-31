import socket  # 소켓 모듈을 임포트합니다.

print("Creating server...")  # 서버 생성 중임을 출력합니다.
s = socket.socket()  # 소켓 객체를 생성합니다.
s.bind(('0.0.0.0', 10000))  # 소켓을 모든 IP 주소와 포트 10000에 바인딩합니다.
s.listen(0)  # 소켓을 듣기 모드로 설정하고 대기열 크기를 0으로 설정합니다.
print("point 1")  # 디버깅을 위한 포인트 1을 출력합니다.

while True:
    client, addr = s.accept()  # 클라이언트의 연결을 수락합니다.
    print("point 2")  # 디버깅을 위한 포인트 2를 출력합니다.
    while True:
        print("point 3")  # 디버깅을 위한 포인트 3을 출력합니다.
        content = client.recv(6)  # 클라이언트로부터 최대 6바이트를 수신합니다.
        if len(content) == 0:
            client.send("uga\n".encode())  # 수신된 데이터가 없으면 "uga" 메시지를 클라이언트로 전송합니다.
            break  # 내부 루프를 종료합니다.
        else:
            print(content.decode())  # 수신된 데이터를 디코드하여 출력합니다.
    #print("Closing connection")  # (주석 처리됨) 연결 종료를 출력하려고 했습니다.
    client.close()  # 클라이언트 소켓을 닫습니다.

    # 얘가 서버