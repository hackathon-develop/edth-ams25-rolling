
# rolling bot


## rpi setup

### image / boot
- https://www.instructables.com/The-Ultimate-Headless-RPi-Zero-Setup-for-Beginners/
- https://forums.raspberrypi.com/viewtopic.php?t=58151 (boot problems)
  - has to show with dmesg

### net
- https://raspberrypi.stackexchange.com/questions/13936/find-raspberry-pi-address-on-local-network
  - manual
- https://www.howtogeek.com/167190/how-and-why-to-assign-the-.local-domain-to-your-raspberry-pi/
  - mDNS apple stuff / install avahi on linux  
    

## hardware components 

### mcu
- https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#introduction

### imu BNO055 (I2C)
- https://www.bosch-sensortec.com/products/smart-sensor-systems/bno055/#documents
- https://www.kiwi-electronics.com/en/adafruit-9-dof-absolute-orientation-imu-fusion-breakout-bno055-stemma-qt-qwiic-10417
- https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/python-circuitpython
- https://github.com/ghirlekar/bno055-python-i2c
- https://github.com/adafruit/Adafruit_CircuitPython_BNO055
  - https://github.com/adafruit/Adafruit_Python_BNO055 (old)
  - https://cdn-learn.adafruit.com/downloads/pdf/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black.pdf
 
### motor driver BTS7960
- https://www.amazon.nl/dp/B07Y4TTK3Z
- https://electronics.stackexchange.com/questions/398556/how-to-control-a-motor-driver-bts7960-without-pwm
- https://community.robotshop.com/forum/t/how-to-i-connect-a-motor-driver-bts7960-43a-to-a-raspberry-pi/69944
  - https://custom-build-robots.com/raspberry-pi-robot-cars/big-rob-motor-driver-bts7960b/8155?lang=en
  - https://forums.raspberrypi.com/viewtopic.php?p=1124139
    - https://github.com/custom-build-robots/Motor-Driver-BTS7960B-and-PCA9685 
- https://www.xsimulator.net/community/threads/2dof-with-45degree-of-roll-and-pitch.18651/

### motors 
- https://www.kiwi-electronics.com/en/dc-motor-with-jst-ph-2-0-connector-37mm-12v-245rpm-10781
- https://www.amazon.nl/-/en/owootecc-torque-Digital-Waterproof-Control/dp/B0819LWL9V
 
### communication receiver elrs
- https://www.bol.com/nl/nl/p/radiomaster-rp3-elrs-2-4ghz-nano-ontvanger/9300000183045489
- https://www.radiomasterrc.com/products/rp3-expresslrs-2-4ghz-nano-receiver

- https://github.com/kaack/elrs-joystick-control

- https://www.youtube.com/watch?v=MCOWKvFTHRc
  - https://github.com/mikeneiderhauser/CRSFJoystick

- https://github.com/i-am-grub/VRxC_ELRS
- https://medium.com/@mike_polo/parsing-crsf-protocol-from-a-flight-controller-with-a-raspberry-pi-for-telemetry-data-79e9426ff943 

- https://github.com/AlfredoSystems/AlfredoCRSF/
  
- https://www.raspberrypi.com/news/building-a-raspberry-pi-pico-2-powered-drone-from-scratch/
  - https://github.com/TimHanewich/scout

- https://blog.cubed.run/fpv-autonomous-flight-with-mavlink-and-raspberry-pi-part-i-f7dfa913f505
- https://medium.com/illumination/fpv-autonomous-flight-with-mavlink-and-raspberry-pi-part-ii-2d55dcd8d659


### battery 
- https://www.amazon.nl/-/en/OVONIC-Battery-5200mAh-Monster-Truggy/dp/B0CX1M6Q4M/


# other projects as reference

- https://www.instructables.com/DIY-Sphere-Robot/
- https://www.instructables.com/DIY-Life-Size-Phone-Controlled-BB8-Droid/
  
- https://youtu.be/6b4ZZQkcNEo

- https://guardbot.org/media/
