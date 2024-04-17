import imp
import numpy as np
import serial


serial_port2 = '/dev/cu.usbmodem141101'#'/dev/cu.usbmodem141101 - IOUSBHostDevice' #'/dev/cu.usbmodem14301' 
baud_rate = 9600

# Create serial connection
ser2 = serial.Serial(serial_port2, baud_rate)
ser2.write('14334'.encode())
