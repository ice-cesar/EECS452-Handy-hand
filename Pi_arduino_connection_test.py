import argparse
import serial
import sys
import time

ser = serial.Serial()
arduino_port = '/dev/ttyACM1'  # Arduino Serial port
# initialize Serial port for Teensy connection
ser.port = arduino_port  # Arduino Serial port
ser.baudrate = 9600
ser.timeout = None  # specify timeout when using readline()
#ser.reset_input_buffer()
time.sleep(3)
print("Serial OK")
ser.open()
time.sleep(0.1);

while True:
    ser.write(b"Hello from Raspberry Pi  \n")
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(1)
ser.close()

