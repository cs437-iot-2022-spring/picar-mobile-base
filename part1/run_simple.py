from picar_4wd import us
from picar_4wd import servo
import picar_4wd as fc

import random
import time
import signal
import sys
# Threshold distance to wall. In cm
THRESHOLD = 20

#Interrupt handler
def signal_handler(signal, frame):
    fc.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def run_simple():
    servo.set_angle(0)
    speed = 15

    while True:
        dist = us.get_distance()
        if dist < THRESHOLD:
            fc.stop()

            time.sleep(.5)
            fc.backward(speed)

            time.sleep(1)

            fc.stop()
            time.sleep(.2)

            direction = random.randrange(2)
            if (direction == 0):
                fc.turn_right(speed / 2)
            else: 
                fc.turn_left(speed / 2)

            time.sleep(.5)

        else:
            fc.forward(speed)


if __name__ == "__main__":
    run_simple()
