import serial

arduino = serial.Serial('COM3', 9600)

while True:
    data = input("0 또는 1을 넣어주세요 : ")
    if data in ['0', '1']:
        arduino.write(data.encode())

