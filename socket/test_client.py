import socket

# 소켓 객체를 생성합니다. (AF_INET: IPv4, SOCK_STREAM: TCP)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결합니다. (IP 주소와 포트 번호를 수정하여 사용하세요)
# c.connect(('172.30.1.98', 5050))
# c.connect(('172.30.1.87', 5050))
c.connect(('172.30.1.5', 5050))

# 서버와 클라이언트는 같은 와이파이에 연결되어 있어야 합니다.
# 서버를 먼저 작동시킨 후 클라이언트를 작동시킵니다. 이때 서버의 IP 주소를 확인합니다.

# 서버와 클라이언트 모두 'exit' 또는 'quit' 같은 단어를 입력받으면 대화를 종료합니다.

while True:
    # 서버에 메시지를 보냅니다.
    # message = "hi"
    message = input("메시지를 입력하세요: ")
    # c.send(message.encode())  # 간단한 메시지를 보낼 때 사용
    c.sendall(message.encode())  # 모든 데이터를 전송할 때 사용
    if message.lower() == 'quit':
        # print("done")
        break

    # 서버로부터 메시지를 받습니다.
    responds = c.recv(1024).decode()
    print(f'받은 메시지 : {responds}')

# 소켓을 닫습니다.
c.close()