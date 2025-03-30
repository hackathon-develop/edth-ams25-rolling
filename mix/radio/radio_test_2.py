import serial
import crsf_parser

# Initialize serial connection to the RP3 receiver
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Initialize the CRSF parser
parser = crsf_parser.CRSFParser(consumer=None)  # You can pass None for now if the consumer is not necessary

# Define a function to handle the controller inputs
def handle_controller_input(packet):
    if packet:
        print("Controller Input Packet Received")
        # Handle telemetry or input data from the packet
        if hasattr(packet, 'stick_values'):
            print(f"Stick Values: {packet.stick_values}")  # If the packet contains stick values
        if hasattr(packet, 'button_states'):
            print(f"Button States: {packet.button_states}")  # If the packet contains button states

# Check available methods and attributes of the CRSFParser
print(dir(parser))

try:
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print(f"Raw Data: {data}")  # Print the raw data for debugging purposes
            
            # Convert bytes to bytearray (mutable)
            data = bytearray(data)
            
            # Feed the raw data to the CRSF parser using parse_stream
            parser.parse_stream(data)

            # Look for the relevant telemetry data in the parser (assuming parser processes packets)
            stats = parser.get_stats()
            if stats:
                print(f"Stats: {stats}")

except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
