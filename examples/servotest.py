import picar_4wd as fc
from picar_4wd import servo
import time

# servo.set_angle(0)

angle = 0
delta = 1
while True:
    if angle >= 90:
        delta = -1
    elif angle <= -90:
        delta = 1
    servo.set_angle(angle)
    angle += delta
    time.sleep(0.01)


