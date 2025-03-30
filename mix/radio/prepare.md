Connect the RP3 receiver to the Raspberry Pi's GPIO pins as follows:​

RP3 Receiver TX → Raspberry Pi GPIO14 (UART RX, Pin 10)
RP3 Receiver RX → Raspberry Pi GPIO15 (UART TX, Pin 8)
RP3 Receiver 5V → Raspberry Pi 5V (Pin 4)
RP3 Receiver GND → Raspberry Pi GND (Pin 6)

sudo raspi-config
Navigate to "Interfacing Options" > "Serial".

Disable the serial console, but enable the serial port.

Reboot your Raspberry Pi:

```python
import serial
from crsf_parser import CRSFParser

# Initialize serial connection to the RP3 receiver
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Initialize the CRSF parser
parser = CRSFParser(consumer=None)  # You can pass None for now if the consumer is not necessary

# Check available methods and attributes of the CRSFParser
print(dir(parser))

try:
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print(data)  # Print the raw data for debugging purposes
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")


```



https://www.youtube.com/watch?v=jOH8YjBTh1k

-----

### **1. Internal Flywheel Mechanism (Gyroscopic Jumping)**
- A high-speed flywheel inside the sphere rapidly decelerates, transferring momentum to the robot and causing it to lift off the ground.
- Example: Some robotic toys and research prototypes use this technique.

- 


### **2. Spring-Loaded Legs or Pistons**
- Hidden spring-loaded legs can extend outward to push off the ground.
- Pneumatic or hydraulic pistons can provide a powerful, controlled jump.
- Example: The "Jumping Sumo" robot from Parrot uses spring-based jumping.

### **3. Reaction Wheels / Mass-Sliding Mechanism**
- An internal mass rapidly shifts upward, forcing the sphere to jump.
- This works similarly to how a person jumps by pushing against the ground.
- Example: Some research robots use internal actuators to move weights quickly.

### **4. Compressed Air / Gas Propulsion**
- A sudden release of compressed air or gas can launch the robot.
- Example: NASA has considered gas-propelled jumping for planetary exploration robots.

### **5. Electromagnetic Actuators**
- Electromagnets inside the sphere repel against the ground, providing a forceful jump.
- This is less common but could be useful in controlled environments.

Would you like a specific jumping mechanism designed for a particular type of spherical robot?


----
- docs/2310.02240v1.pdf
```
    One potential solution to address this
    challenge is incorporating jumping mechanisms in spherical robots, enabling them to overcome obstacles vertically. By introducing a jumping mechanism, spherical
    robots gain the ability to leap over barriers, gaps, or rough
    terrain that would otherwise be challenging or impossible to traverse with rolling or sliding locomotion alone.
    However, achieving controlled leaps while managing the
    position of the center of mass and the point of application
    of the propulsion force remains an open challenge due to
    the mechanical complexity involved.


    ....

    Mizumura, Y., Ishibashi, K., Yamada, S., Takanishi, A., and Ishii, H., 2018, “Mechanical design of
    a jumping and rolling spherical robot for children
    with developmental disorders,” 2017 IEEE International Conference on Robotics and Biomimetics,
    ROBIO 2017, 2018-Janua, pp. 1–6.

    ....

    Sugiyama, Y., and Hirai, S., 2006, “Crawling and
    jumping by a deformable robot,” International
    Journal of Robotics Research, 25(5-6), pp. 603–
    620.
```

```

```
