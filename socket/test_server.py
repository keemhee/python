#socket 열기
import socket

#host_name = socket.gethostname()
#ip_address = socket.gethostbyname(host_name)
#print(f'HOST: {host_name}')
#print(f'IP ADDRESS: {ip_address}')

#server는 host, ip address => 제공
#client는 요청

#보통 함수로 만듦
#try: 
# 엔터 해야할 코드
#except Exception as e:
#  print("ip address 없습니다.")  처리할 코드
#  print(f"{e}")
#어느 지점에서 어느 에러가 떴는지 확인하기 편함

def get_ip_address():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print(f'{host_name}: {host_ip}')
        return host_ip    
    except Exception as e:
        print(f"{e}")

host_ip = get_ip_address()
print(host_ip)

#server는 본인 거 알아서 bind 해야 함.
#client는 server의 address를 connect한다

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #AF_INET : IPv4를 쓴다.
server.bind((host_ip, 5050))     #이렇게 하면  server_bind가 된다.
#print("ok")
#client가 언제 요청할 지 모르니까 계속  listen 하고 있어야함.
server.listen(5)
c_socket, c_address = server.accept() #클라이언트의 커넥트를 받는 거. 한 번만 되게  while문에서 빼주기.
while True:
    #client의 address와 name을 받을 거
    
    print(c_address)
    #client가 보낸 메시지 받기
    message = c_socket.recv(1024).decode()
    print(f'받은 메시지 : {message}')
   # if message.lower() == 'exit' or 'quit':
        #print("done")
    #    break
    #client에게 답장보내기
    #respond = "Fine Thank you and you?"
    respond = input("메시지를 입력하세요: ")
    #c_socket.send(respond.encode())
    c_socket.sendall(respond.encode())

#server.close

