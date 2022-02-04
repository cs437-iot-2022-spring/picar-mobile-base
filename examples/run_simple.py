from picar_4wd import us
from picar_4wd import servo
import picar_4wd as fc

import random
import signal
import sys
# Threshold distance to wall. In cm
THRESHOLD = 20

# How many loop iterations to turn for. 
TURN_DURATION = 500

#Interrupt handler
def signal_handler(signal, frame):
    fc.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def run_simple():
    servo.set_angle(0)
    speed = 40

    curr_turn_duration = 0
    # 0: Left, 1: Right
    curr_turn_direction = 0
    
    while True:

        if curr_turn_duration > 0:
            if curr_turn_direction == 0:
                fc.turn_left(speed)
            elif curr_turn_direction == 1:
                fc.turn_right(speed)

            curr_turn_duration -= 1
        else:
            dist = us.get_distance()

            if dist < THRESHOLD:
                print("AHHHHHHHHHHHHHHHHHHHHH")
                direction = random.randrange(2)

                curr_turn_duration = TURN_DURATION

            fc.forward(speed)


if __name__ == "__main__":
    run_simple()
