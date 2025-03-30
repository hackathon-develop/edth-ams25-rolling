import serial
import struct
import time

# === Serial Setup ===
ser = serial.Serial("/dev/serial0", 420000, timeout=1)

# === Filtering Parameters ===
DEADZONE = 0.05
SMOOTHING = 0.2

# === Previous filtered values ===
prev_throttle = 0.0
prev_steering = 0.0

# === Helper Functions ===

def normalize(val):
    """Convert 1000–2000 to -1.0 to 1.0"""
    return max(-1.0, min(1.0, (val - 1500) / 500.0))

def apply_deadzone(val, threshold=DEADZONE):
    return 0.0 if abs(val) < threshold else val

def lerp(prev, new, alpha=SMOOTHING):
    return prev + (new - prev) * alpha

def read_crsf_frame():
    """Reads one full CRSF frame and returns raw channels"""
    while True:
        byte = ser.read()
        if byte == b'\xC8':  # Start of CRSF frame
            length = ser.read()[0]
            payload = ser.read(length)
            if payload[0] == 0x16:  # RC channels frame
                # Ensure the payload has the correct number of bytes
                if len(payload) >= 22:  # CRSF frame should be at least 22 bytes for RC data
                    data = payload[2:22]
                    try:
                        channels = struct.unpack("<HHHHHHHH", data)
                        return channels
                    except struct.error as e:
                        print(f"Error unpacking CRSF frame: {e}")
                        continue  # Skip this frame and try reading again
                else:
                    print("Warning: Incomplete CRSF frame received.")
                    continue  # Skip incomplete frames

# === Main Loop ===
print("🛰️  Listening for CRSF joystick data...")

while True:
    try:
        rc = read_crsf_frame()

        raw_throttle = rc[0]  # CH1: throttle
        raw_roll     = rc[1]  # CH2: roll (steering)

        # Normalize
        norm_throttle = normalize(raw_throttle)
        norm_roll = normalize(raw_roll)

        # Deadzone
        throttle = apply_deadzone(norm_throttle)
        roll = apply_deadzone(norm_roll)

        # Smoothing
        throttle = lerp(prev_throttle, throttle)
        roll = lerp(prev_steering, roll)
        prev_throttle = throttle
        prev_steering = roll

        # Detect active joystick movement
        throttle_active = abs(throttle) > 0
        roll_active = abs(roll) > 0

        # === OUTPUT ===
        print(f"Throttle: {throttle:+.2f} {'(Active)' if throttle_active else ''} | Roll: {roll:+.2f} {'(Active)' if roll_active else ''}")

        # You can now use `throttle` and `roll` to control motors!
        # Example:
        # motor_left.value = clamp(throttle + roll)
        # motor_right.value = clamp(throttle - roll)

        time.sleep(0.05)

    except Exception as e:
        print("Error:", e)
