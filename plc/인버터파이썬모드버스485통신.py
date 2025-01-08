from pymodbus.client import ModbusSerialClient
# PLC 초기화
port = 'COM5'  # PLC의 시리얼 포트
baudrate = 9600  # PLC의 시리얼 속도
bytesize = 8  # PLC의 불류 크기
parity = 'N'  # PLC의 패리티
stopbits = 1  # PLC의 스톱 비트
timeout = 3  # PLC의 타임아웃 시간
# Modbus 클라이언트 초기화
client = ModbusSerialClient(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout)
# 접속 확인
if client.connect():
    print("접속 성공")
    # PLC 메모리에 접근
    # PLC 메모리에 데이터 쓰기
    while(1):
        a = int(input('mode 5057정지, 5058, 5060 >> '))
        result = client.write_register(5, a, slave=2)
    print(result)
    # 접속 종료
    client.close()
else:
    print("접속 실패")
'''
6:22
485+ -> A
485- -> B
client.write_register()
주소 10진수로 쓰면
plc의 경우 D영역
인버터의 경우 4 - freq / 5 - 기동 / 6 - 가속 / 7 - 감속
'''