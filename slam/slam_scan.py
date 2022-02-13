import numpy as np
from picar_4wd import us
from picar_4wd import servo
import time
import cv2

MAX_RANGE = 120 # r=200cm
SIZE = (MAX_RANGE,2*MAX_RANGE)
MIN_ANGLE = -90
MAX_ANGLE = 90

CLEARANCE = 3

def cart_from_polar(r, theta):
    """Make sure theta is in radians"""
    return r * np.cos(theta), r * np.sin(theta)

def record_obstacle(r, theta, arr):
    if (r > MAX_RANGE):
        r = MAX_RANGE-CLEARANCE
    elif (r < 0):
        r = MAX_RANGE-CLEARANCE

    rad = (theta/180.0)*np.pi 
    x, y = cart_from_polar(r, rad + (np.pi/2))
    arr[int(y), int(x + MAX_RANGE)] = 0
    
    return np.array([x,y])

def linear_interpolate(x1, x2, arr):
    d = np.linalg.norm(x2-x1)
    alphas = np.linspace(0,1,round(128 * d))
    for a in alphas:
        x, y = a*x1 + (1-a)*x2
        arr[round(y), round(x + MAX_RANGE)] = 0    

def add_to_queue(q,arr,S,point):
    x,y=point
    if point not in S and x>=0 and x<arr.shape[1] and y>=0 and y<arr.shape[0]:
        q.append(point)
        S.add(point)

def flood_fill(arr,start):
    visited = set([start])
    q = [start]
    while len(q):
        x,y = q.pop(0)
        if arr[y,x] == 0:
            continue
        arr[y,x] = 0
        add_to_queue(q,arr,visited,(x+1,y))
        add_to_queue(q,arr,visited,(x,y+1))
        add_to_queue(q,arr,visited,(x-1,y))
        add_to_queue(q,arr,visited,(x,y-1))


def sweep(left_to_right=True):
    """
    @param: left_to_right - True or False
    """
    arr = np.ones(SIZE) # Initialize map of ones
    step_multiplier = (1-2*left_to_right) # Returns 1 or -1 depending on rotation

    servo.set_angle(MIN_ANGLE * step_multiplier)
    dist = us.get_distance()
    x = record_obstacle(dist, MIN_ANGLE * step_multiplier, arr)
    for angle in range(MIN_ANGLE * step_multiplier, MAX_ANGLE * step_multiplier, step_multiplier):
        servo.set_angle(angle)
        dist = us.get_distance()
        x1 = record_obstacle(dist, angle, arr)
        linear_interpolate(x1, x, arr)
        x = x1
        time.sleep(0.01)
    print(x)
    linear_interpolate(x,np.array([x[0],0]),arr)
    cv2.imwrite("prefill-image.jpg", 255*np.flip(arr,axis=0))
    flood_fill(arr,(MAX_RANGE,0))
    
    return arr

def print_map(arr):
    # print(np.array2string(map))
    print(arr)
    
def map_to_video(arr):
    pass


if __name__ == "__main__":
    print("Starting")
    arr = sweep(left_to_right=1)
    np.save("map", arr)

    im = (np.array(arr * 255, dtype = np.uint8))
    im = np.flip(im, axis=0)
    
    # threshed = cv2.threshold(im,1,255,cv2.THRESH_BINARY)
    # threshed = threshold(im)
    cv2.imwrite("image.jpg", im)
    print("Image Saved")

    # add_boundary(map, 0)


    # print(arr)
    # arr = sweep(left_to_right=-1)
    # draw_map(map)
    # print(arr)