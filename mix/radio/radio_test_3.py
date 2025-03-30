import serial
import struct

# Adjust if using another UART (e.g., /dev/serial0 or /dev/ttyAMA0)
ser = serial.Serial("/dev/serial0", 420000, timeout=1)

def read_crsf_frame():
    while True:
        byte = ser.read()
        if byte == b'\xc8':  # CRSF sync byte
            length = ser.read()[0]
            payload = ser.read(length)
            if payload[0] == 0x16:  # RC Channels frame
                data = payload[2:22]
                channels = struct.unpack("<HHHHHHHH", data)
                return channels  # 16-bit values, 8 channels

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
