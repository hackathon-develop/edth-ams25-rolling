import serial
from crsf_parser import CRSFParser

# Initialize serial connection to the RP3 receiver
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Initialize the CRSF parser
parser = CRSFParser(consumer=None)  # You can pass None for now if the consumer is not necessary

# Check available methods and attributes of the CRSFParser
print(dir(parser))

try:
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print(data)  # Print the raw data for debugging purposes
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
