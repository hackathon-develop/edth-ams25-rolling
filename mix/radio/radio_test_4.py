import serial
import struct

# Adjust if using another UART (e.g., /dev/serial0 or /dev/ttyAMA0)
ser = serial.Serial("/dev/serial0", 420000, timeout=1)

def read_crsf_frame():
    while True:
        byte = ser.read()
        if byte == b'\xc8':  # CRSF sync byte
            length = ser.read()[0]
            if length == 0:
                continue  # Skip if length is zero or invalid frame
            
            payload = ser.read(length)
            
            # Check if the frame is correct and has at least the expected length
            if len(payload) >= 6:  # Assuming 22 bytes for the RC Channels frame
                if payload[0] == 0x16:  # RC Channels frame
                    data = payload[2:22]  # Extract the data part
                    if len(data) == 16:  # Ensure we have 16 bytes for unpacking
                        channels = struct.unpack("<HHHHHHHH", data)  # Unpack channels
                        return channels  # 16-bit values, 8 channels
                else:
                    print("hurts 1")  # Skip if it's not the expected frame type
                    continue  # Skip if it's not the expected frame type
            else:
                continue  # Skip if payload length is less than expected

while True:
    try:
        rc = read_crsf_frame()
        throttle = rc[0]  # Usually channel 0 (1000–2000)
        yaw = rc[1]       # Channel 1
        pitch = rc[2]
        roll = rc[3]

        print(f"Throttle: {throttle}, Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}")

    except Exception as e:
        print("Error:", e)
