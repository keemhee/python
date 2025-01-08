import websocket

# Connect to WebSocket server
ws = websocket.WebSocket()     # WebSocket 객체 생성
ws.connect("ws://172.30.1.10") # ESP32 서버의 IP 주소와 연결
print("Connected to WebSocket server")



while True:
    # 사용자의 입력을 받아 서버로 전송
    str_input = input("Say something (or type 'exit' to quit): ")
    
    if str_input.lower() == 'exit':
        print("Closing connection...")
        ws.close()
        break
    
    # 메시지를 서버로 전송
    ws.send(str_input)
    print(f"Sent: {str_input}")

    # 서버로부터 응답 수신
    result = ws.recv()
    print(f"Received: {result}")

