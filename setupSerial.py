import serial.tools.list_ports

# Get a list of all available serial ports
ports = serial.tools.list_ports.comports()

# Print information about each serial port
for port in ports:
    print(port)