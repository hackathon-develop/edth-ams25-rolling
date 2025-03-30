import serial
from crsf_parser import CRSFParser

# Initialize serial connection to the RP3 receiver
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Initialize the CRSF parser
parser = CRSFParser()

try:
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            parser.feed(data)
            for packet in parser.get_packets():
                # Process the CRSF packet
                print(packet)
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
