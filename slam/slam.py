import numpy as np
from picar_4wd import us
from picar_4wd import servo
import time

SIZE = (200,400)
MAX_RANGE = 200 # 200cm
MIN_ANGLE = -90
MAX_ANGLE = 90

def cart_from_polar(r, theta):
    """Make sure theta is in radians"""
    return r * np.cos(theta)

def record_obstacle(r, theta, map):
    if (r > MAX_RANGE):
        # print("Distance exceeded max range")
        return
    rad = (theta/180.0)*np.pi
    x, y = cart_from_polar((r, rad))
    map[x + MAX_RANGE, y] = 1
    for d in range(0, int(r)): # vectorize this sometime
        x,y = cart_from_polar((d, rad))
        map[x + MAX_RANGE, y] = 0


def sweep(left_to_right=1):
    """
    @param: left_to_right - 1 if true, -1 if false
    """
    map = np.ones(SIZE)
    for angle in range(MIN_ANGLE * left_to_right, MAX_ANGLE * left_to_right, left_to_right):
        servo.set_angle(angle)
        dist = us.get_distance()
        record_obstacle(dist, angle, map)
        time.sleep(0.01)
    
    return map

def print_map(map):
    # print(np.array2string(map))
    print(map)
    
def map_to_video(map):
    pass

if __name__ == "__main__":
    map = sweep(left_to_right=1)
    # draw_map(map)
    print(map)
    map = sweep(left_to_right=-1)
    # draw_map(map)
    print(map)