lsusb for mac :
~~~
ioreg -p IOUSB -l -w 0 | grep "IORegistryEntryName" | awk -F '"' '{print $4}'
~~~



shivergard: Install Adafruite library :
~~~
python3 -m venv ball 
source ball/bin/activate
pip install adafruit-circuitpython-pca9685 
~~~
 



ilya@applepie:~ $ history
~~~
    1  ls
    2  sudo apt update
    3  sudo apt install python3-pip -y
    4  pip3 install adafruit-circuitpython-pca9685
    5  sudo apt install python3-venv -y
    6  python3 -m venv ~/pca9685-env
    7  python3 -m venv ~/grogu
    8  s
    9  python3 -m venv ~/grogu
   10  source ~/grogu/bin/activate
   11  pip install adafruit-circuitpython-pca9685 adafruit-blinka
   12  nano move_servo.py
   13  python move_servo.py
   14  rm move_servo.py 
   15  nano move_servo.py
   16  python move_servo.py 
   17  sudo raspi-config
   18  python move_servo.py 
   19  rm move_servo.py 
   20  nano move_servo.py
   21  pip install keyboard
   22  python move_servo.py 
   23  rm move_servo.py 
   24  nano move_servo.py
   25  python move_servo.py 
   26  sudo apt install -y i2c-tools
   27  sudo i2cdetect -y 1
   28  rm move_servo.py 
   29  nano move_servo.py
   30  python move_servo.py 
   31  sudo apt install python3-gpiozero
   32  nano dc_test.py
   33  python dc_test.py
   34  pip install gpiozero
   35  python dc_test.py
   36  nano dc_test.py
   37  python dc_test.py
   38  history
~~~



illya: DC code:
~~~
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

# Define motor control pins (update if needed)
# Left Motor
left_pwm = PWMOutputDevice(12)   # L_PWM
left_en = DigitalOutputDevice(22)  # L_EN

# Right Motor
right_pwm = PWMOutputDevice(13)  # R_PWM
right_en = DigitalOutputDevice(23)  # R_EN

# Enable both motors
left_en.on()
right_en.on()

# Set speed (10% = 0.1)
speed = 0.1

print("Running both motors at 10% speed for 5 seconds...")
left_pwm.value = speed
right_pwm.value = speed

sleep(5)

# Stop motors
left_pwm.value = 0
right_pwm.value = 0
left_en.off()
right_en.off()
print("Motors stopped.")
`
[3:36 AM]illya: Servo code:
`
import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Setup
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50
channel = 0

# Updated angle function
def angle_to_pwm(angle):
    min_pulse = 500
    max_pulse = 2500
    pulse = min_pulse + (angle / 180.0) * (max_pulse - min_pulse)
    return int((pulse / 20000) * 65535)

# Move to desired angle
desired_angle = 90
pca.channels[channel].duty_cycle = angle_to_pwm(desired_angle)
print(f"Moved to {desired_angle}°")
time.sleep(2)

pca.deinit()
~~~


illya:
~~~
pip install adafruit-circuitpython-bno055
~~~


illya:
~~~
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
~~~


illya:
~~~
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
                data = payload[2:22]
                channels = struct.unpack("<HHHHHHHH", data)
                return channels

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
        print(f"Throttle: {throttle:+.2f} {"if throttle_active else ''}  |  Roll: {roll:+.2f} {"if roll_active else ''}")

        # You can now use `throttle` and `roll` to control motors!
        # Example:
        # motor_left.value = clamp(throttle + roll)
        # motor_right.value = clamp(throttle - roll)

        time.sleep(0.05)

    except Exception as e:
        print("Error:", e)
~~~~

radio.zip

https://github.com/samfok/remote_receiver_tutorial/blob/master/main.py



~~~
#!/usr/bin/env python3
import serial
import time
import argparse

CRSF_SYNC = 0xC8
RC_CHANNELS_PACKED = 0x16

def crc8_dvb_s2(crc, a) -> int:
  crc = crc ^ a
  for ii in range(8):
    if crc & 0x80:
      crc = (crc << 1) ^ 0xD5
    else:
      crc = crc << 1
  return crc & 0xFF

def crc8_data(data) -> int:
    crc = 0
    for a in data:
        crc = crc8_dvb_s2(crc, a)
    return crc

def crsf_validate_frame(frame) -> bool:
    return crc8_data(frame[2:-1]) == frame[-1]

def unpack_channel_values(data: bytearray) -> list:
    """
    Skips first 3 bytes, then unpacks 16 11-bit channels from the next 22 bytes.
    
    Args:
        data (bytearray): Bytearray containing at least 25 bytes (3 skip + 22 data)
        
    Returns:
        list: List of 16 unsigned integers, each representing an 11-bit channel value
    """
    working_data = data[3:25]
    
    result = []
    bit_position = 0
    
    for i in range(16):
        # Calculate which bytes we need to read from
        byte_index = bit_position // 8
        bit_offset = bit_position % 8
        
        # Read enough bytes to cover our 11 bits
        value = 0
        for j in range(3):  # We might need up to 3 bytes to get our 11 bits
            if byte_index + j < len(working_data):
                value |= working_data[byte_index + j] << (8 * j)
        
        # Shift right to align to start of our 11 bits and mask to get only 11 bits
        value = (value >> bit_offset) & 0x7FF
        result.append(value)
        bit_position += 11
    
    return result

def pack_channels(channels: list) -> bytearray:
    """
    Packs 16 11-bit channel values into 22 bytes.
    
    Args:
        channels (list): List of 16 integers, each representing an 11-bit channel value (0-2047)
        
    Returns:
        bytearray: 22 bytes containing the packed 11-bit values
    """
    if len(channels) != 16:
        raise ValueError("Must provide exactly 16 channel values")
        
    # Validate channel values
    for i, value in enumerate(channels):
        if not 0 <= value <= 2047:  # 2047 is max value for 11 bits (0x7FF)
            raise ValueError(f"Channel {i+1} value {value} exceeds 11-bit range (0-2047)")
    
    result = bytearray(22)  # Initialize empty 22-byte array
    bit_position = 0
    
    for value in channels:
        # Calculate which bytes we need to write to
        byte_index = bit_position // 8
        bit_offset = bit_position % 8
        
        # Shift value to its bit position
        shifted_value = value << bit_offset
        
        # Write the value across the necessary bytes
        for j in range(3):  # Might need up to 3 bytes per value
            if byte_index + j < len(result):
                # Mask out the bits we're about to write
                mask = (0xFF << bit_offset if j == 0 else 0xFF) if j < 2 else 0xFF
                # Clear the bits we're about to write
                result[byte_index + j] &= ~mask
                # Write the new bits
                result[byte_index + j] |= (shifted_value >> (8 * j)) & 0xFF
        
        bit_position += 11
    return result

def generate_frame(roll : int, pitch : int, yaw : int, throttle : int, armed : int, custom : int) -> bytes:
    channeldata = [roll, pitch, yaw, throttle, armed, custom]
    for i in range(6,16):
      channeldata.append(992)
    result = [CRSF_SYNC,24,RC_CHANNELS_PACKED]
    result += pack_channels(channeldata)
    result.append(crc8_data(result[2:]))
    return result

#Switch between microseconds and 11-bit Value and vise versa
def get_us(crsf) -> int:
    return int(1500 + (5/8 * (crsf - 992)))
def get_crsf(us) -> int:
    return int(992 + (8/5 * (us - 1500)))



parser = argparse.ArgumentParser()
parser.add_argument('-P', '--port', default='/dev/ttyAMA0', required=False)
parser.add_argument('-b', '--baud', default=420000, required=False)
args = parser.parse_args()

with serial.Serial(args.port, args.baud, timeout=2) as ser:
    while True:
        # Receive a Frame and decode it
        input = bytearray()
        if ser.in_waiting > 0:
            input.extend(ser.read(ser.in_waiting))
        else:
            time.sleep(0.020)

        if len(input) > 2:
            expected_len = input[1] + 2
            if crsf_validate_frame(input[:expected_len]):
                    if input[2] == RC_CHANNELS_PACKED:
                        received = unpack_channel_values(input)
                        print(received)
                        # received_us = []
                        # for i in range(len(received)):
                        #     us = get_us(received[i])
                        #     received_us.append(us)
                        # print(f"Microseconds:{received_us}")
        # Generate a frame and send it
        frame = generate_frame(111,222,333,444,555,666)
        ser.write(frame)
        time.sleep(0.020)
~~~