# server 
import socket  # 소켓 모듈을 임포트
 
def get_ip_address():  # IP 주소를 가져오는 함수 정의 
    try:
        host_name = socket.gethostname()  # 호스트 이름을 가져옴
        host_ip = socket.gethostbyname(host_name)  # 호스트 이름으로 IP 주소를 가져옴
        print(f'{host_name} : {host_ip}')  # 호스트 이름과 IP 주소를 출력
        return host_ip  # IP 주소를 반환
        
    except Exception as e:  # 예외 발생 시
   	    print(f"{e}")  # 예외 메시지를 출력 
host_ip = get_ip_address()  # IP 주소를 가져와서 변수에 저장
print(host_ip)  # IP 주소를 출력

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓 객체를 생성
server.bind((host_ip, 5050))  # 소켓을 IP 주소와 포트에 바인딩
print("ok")  # 바인딩 성공 메시지 출력
server.listen(5)  # 클라이언트의 연결을 대기
c_socket, c_address = server.accept()  # 클라이언트의 연결을 수락
while True:  # 무한 루프 시작
 
     
     message = c_socket.recv(1024).decode()  # 클라이언트로부터 메시지를 수신하고 디코딩
     
     if message == 'quit':  # 수신한 메시지가 'quit'이면
          break  # 루프를 종료

     print(f'client message : {message}')  # 클라이언트 메시지를 출력

     respond = input("클라이언트에게 보낼 메세지 : ")  # 사용자로부터 응답 메시지를 입력받음
     c_socket.sendall(respond.encode())  # 응답 메시지를 인코딩하여 클라이언트에게 전송

server.close()  # 서버 소켓을 닫음
