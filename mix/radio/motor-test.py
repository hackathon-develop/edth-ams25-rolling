import time

try:
    from gpiozero import PWMOutputDevice, DigitalOutputDevice
    REAL_HARDWARE = True
except ImportError:
    # Mock classes for simulation
    REAL_HARDWARE = False
    class PWMOutputDevice:
        def __init__(self, pin):
            self.pin = pin
            self.value = 0
        
        def __repr__(self):
            return f"MockPWMOutputDevice(pin={self.pin}, value={self.value})"
    
    class DigitalOutputDevice:
        def __init__(self, pin):
            self.pin = pin
            self.state = False
        
        def on(self):
            self.state = True
            print(f"Mock DigitalOutputDevice(pin={self.pin}) turned ON")
        
        def off(self):
            self.state = False
            print(f"Mock DigitalOutputDevice(pin={self.pin}) turned OFF")
        
        def __repr__(self):
            return f"MockDigitalOutputDevice(pin={self.pin}, state={self.state})"

# Define motor control pins (update if needed)
left_pwm = PWMOutputDevice(12)  # L_PWM
left_en = DigitalOutputDevice(22)  # L_EN
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

# Simulate runtime
time.sleep(5)

# Stop motors
left_pwm.value = 0
right_pwm.value = 0
left_en.off()
right_en.off()
print("Motors stopped.")
