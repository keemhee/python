import websocket

# Connect to WebSocket server
ws = websocket.WebSocket()     #ws는 클래스 객체
ws.connect("ws://172.30.1.10") #클라이언트니까 어디 접속할 건지 여기에 넣어줌.
print("Connected to WebSocket server")


#for i in range(5):
    #srt = input("Enter password: ")
    #ws.send(str)
    

# Ask the user for some input and transmit it
str = input("Say something: ") #콘솔인풋받은 거 보내기
ws.send(str)

# Wait for server to respond and print it
result = ws.recv()
print("Received: " + result)

# Gracefully close WebSocket connection
ws.close()

