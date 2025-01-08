import socket

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#c.connect(('172.30.1.98', 5050))
#c.connect(('172.30.1.87', 5050))
c.connect(('172.30.1.5', 5050))
#print("ok")

#서버랑 클라이언트 같은 와이파이
#서버 먼저 작동
#클라이언트 작동. ip주소 확인.


#서버, 클라이언트 모두 'exit', 'quit'같은 단어 input을 받으면 대화 끝나게.

while True:
    #서버에 메시지보내기
    #message = "hi"
    message = input("메시지를 입력하세요: ")
    #c.send(message.encode()) 간단한 메시지
    c.sendall(message.encode())
    if message.lower() == 'quit':
        #print("done")
        break
    #서버한테 온 메시지 받기
    responds = c.recv(1024).decode()
    print(f'받은 메시지 : {responds}')

c.close