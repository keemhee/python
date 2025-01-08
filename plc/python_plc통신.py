import serial

ser = serial.Serial('COM6', 9600, timeout=1)

read = 0

print("Start")
print(ser.name)

ser.write(b'\x0501WSS0106%PW004003f\x04') # 0003 -> 8421 8421 8421 8421. 램프 총 16개. 1번 2번 램프 켜겠다.(15번 켜려면 4000, 6번 켜려면 0020)
# w가 r이 되면 plc의 데이터 읽어옴
print("Reading")
read = ser.readline().decode('ascii')
print("Reading: ", read)

ser.close()

'''import serial

ser = serial.Serial('COM6', 9600, timeout=1)

read = 0

print("Start")
print(ser.name)

ser.write(b'\x0501RSS0106%PW0040003\x04')

print("Reading")
read = ser.readline().decode('ascii')
print("Reading: ", read)

ser.close()'''
