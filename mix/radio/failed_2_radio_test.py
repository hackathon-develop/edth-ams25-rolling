import serial
from crsf_parser import CRSFParser

# Define a consumer function to process the parsed data
def process_packet(packet):
    # Handle the packet data here
    print(packet)

# Initialize serial connection to the RP3 receiver
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Initialize the CRSF parser with the consumer function
parser = CRSFParser(consumer=process_packet)

try:
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            parser.feed(data)
            # No need for parser.get_packets() since packets are processed by the consumer directly
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
