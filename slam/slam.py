import numpy as np
from picar_4wd import us
from picar_4wd import servo
import time

MAX_RANGE = 200 # r=200cm
SIZE = (MAX_RANGE,2*MAX_RANGE)
MIN_ANGLE = -90
MAX_ANGLE = 90

def cart_from_polar(r, theta):
    """Make sure theta is in radians"""
    return r * np.cos(theta)

def record_obstacle(r, theta, arr):
    if (r > MAX_RANGE):
        r = MAX_RANGE

    rad = (theta/180.0)*np.pi
    x, y = cart_from_polar((r, rad))
    arr[x + MAX_RANGE, y] = 1
    for d in range(0, int(r)): # vectorize this sometime
        x,y = cart_from_polar((d, rad))
        arr[x + MAX_RANGE, y] = 0


def sweep(left_to_right=True):
    """
    @param: left_to_right - True or False
    """
    arr = np.ones(SIZE) # Initialize map of ones
    step_multiplier = (1-2*left_to_right) # Returns 1 or -1 depending on rotation

    for angle in range(MIN_ANGLE * step_multiplier, MAX_ANGLE * step_multiplier, step_multiplier):
        servo.set_angle(angle)
        dist = us.get_distance()
        record_obstacle(dist, angle, arr)
        time.sleep(0.01)
    
    return arr

def print_map(arr):
    # print(np.array2string(map))
    print(arr)
    
def map_to_video(arr):
    pass

if __name__ == "__main__":
    arr = sweep(left_to_right=1)
    # draw_map(map)
    print(arr)
    arr = sweep(left_to_right=-1)
    # draw_map(map)
    print(arr)