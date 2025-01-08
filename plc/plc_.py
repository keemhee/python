from pymodbus.client import ModbusSerialClient

# 485통신 연결 설정
port = 'COM3'  # USB 시리얼 포트
baudrate = 9600  # 시리얼 속도
bytesize = 8  #5, 6, 7, 8 가능인데 모드버스에선 거의 8을 씀
parity = 'N'  #패리티 안 씀
stopbits = 1
timeout = 3  #plc연결 3초이내에 안 되면 끊어짐

# Modbus 클라이언트 초기화
client = ModbusSerialClient(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout)

# 접속 확인
if client.connect():
    print("접속 성공")

    # INV 메모리에 데이터 쓰기, 인버터 설정 모드버스 485통신 사용 설정
    # inv 주소 4-주파수 / 5-가동 / 6-가속 / 7-감속
    # slave= 여기에 인버터 국번 입력
    client.write_register(4, 4000, slave=2) # 4000 -> 40Hz
    client.write_register(6, 10, slave=2)   # 10 -> 1초
    client.write_register(7, 20, slave=2)   # 20 -> 2초

    while(1):   # 무한반복
        a = int(input('mode 5057정지, 5058, 5060 ( -1 입력시 정지 )>> '))
        if(a == -1):
            break
        result = client.write_register(5, a, slave=2)

    # 접속 종료
    client.close()
else:
    print("접속 실패")
