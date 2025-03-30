### root

# sudo -i
# apt-get update
# # apt-get upgrade
# apt install pip

### user

# cd src
# python3 -m venv .venv
# source .venv/bin/activate
# pip install Adafruit_PCA9685     dont do this
# pip3 install adafruit-circuitpython-pca9685



# https://www.kevsrobots.com/learn/pca9685/05_setting_up_the_pca9685_with_raspberry_pi.html  (partly outdated)
# -> https://github.com/adafruit/Adafruit_Python_PCA9685/issues/20
# -> https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython

import board
import busio
# from Adafruit_PCA9685 import PCA9685
import adafruit_pca9685

from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
# Step 2: Initialize PCA9685
# pwm = adafruit_pca9685.PCA9685()
pwm = pca
pwm.set_pwm_freq(60)  # Set frequency to 60Hz


# Step 3: Control a Servo
# We’ll make the servo connected to channel 0 move back and forth.

channel = 0
min_pulse = 150  # Min pulse length out of 4096
max_pulse = 600  # Max pulse length out of 4096

while True:
    pwm.set_pwm(channel, 0, min_pulse)
    sleep(1)
    pwm.set_pwm(channel, 0, max_pulse)
    sleep(1)
