import socket

print("Creating server...")
s = socket.socket()
s.bind(('0.0.0.0', 10000))
s.listen(0)
print("point 1")

while True:
    client, addr = s.accept()
    print("point 2")
    while True:
        print("point 3")
        content = client.recv(6)
        if len(content) == 0:
            client.send("uga\n".encode())
            break
        else:
            print(content.decode())
    #print("Closing connection")
    client.close()

    # 얘가 서버