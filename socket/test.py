#Server  # 서버 스크립트임을 나타내는 주석

import socket  # 소켓 모듈을 임포트합니다.

def get_ip_address():  # IP 주소를 얻는 함수를 정의합니다.
    
    try:
        host_name = socket.gethostname()  # 호스트 이름을 가져옵니다.
        host_ip = socket.gethostbyname(host_name)  # 호스트 이름을 통해 IP 주소를 가져옵니다.
        print(f'{host_name} : {host_ip}')  # 호스트 이름과 IP 주소를 출력합니다.
        return host_ip  # IP 주소를 반환합니다.
        
    except Exception as e:
        print(f"{e}")  # 예외가 발생하면 예외 메시지를 출력합니다.

host_ip = get_ip_address()  # IP 주소를 얻어서 변수에 저장합니다.
print(host_ip)  # IP 주소를 출력합니다.

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 주소체계와 TCP 프로토콜을 사용하는 소켓을 생성합니다.
server.bind((host_ip, 5050))  # 소켓을 IP 주소와 포트 5050에 바인딩합니다.
print("ok")  # 바인딩이 성공했음을 출력합니다.
server.listen(5)  # 소켓을 듣기 모드로 설정하고 최대 5개의 연결을 대기합니다.

c_socket, c_address = server.accept()  # 클라이언트의 연결을 수락합니다.

while True:
    message = c_socket.recv(1024).decode()  # 클라이언트로부터 최대 1024바이트의 메시지를 수신하고 디코드합니다.
    
    if message == 'quit':
        c_socket.sendall(message.encode())  # 메시지가 'quit'이면 클라이언트에게 다시 전송합니다.
        break  # 루프를 종료합니다.

    print(f'client message : {message}')  # 클라이언트로부터 받은 메시지를 출력합니다.

    respond = input("클라이언트에게 보낼 메세지 : ")  # 사용자에게 보낼 메시지를 입력받습니다.
    c_socket.sendall(respond.encode())  # 입력받은 메시지를 클라이언트에게 전송합니다.

server.close()  # 서버 소켓을 닫습니다.