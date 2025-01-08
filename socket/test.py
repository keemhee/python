#Server

import socket

def get_ip_address():

    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print(f'{host_name} : {host_ip}')
        return host_ip
        
    except Exception as e:
   	    print(f"{e}")
 
host_ip = get_ip_address() 
print(host_ip) 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host_ip, 5050))
print("ok")
server.listen(5)

c_socket, c_address = server.accept()     
     
while True:
     message = c_socket.recv(1024).decode()
     
     if message == 'quit':
          c_socket.sendall(message.endcode())
          break

     print(f'client message : {message}')

     respond = input("클라이언트에게 보낼 메세지 : ")
     c_socket.sendall(respond.encode())

server.close()