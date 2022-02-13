import numpy as np
import cv2
from numpy.linalg import norm
import picar_4wd as fc
import time

import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import signal
import sys

#Interrupt handler
def signal_handler(signal, frame):
    fc.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


class Node():
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        self.dist = 0
        self.h = 0
        self.cost = 0

    def __eq__(self, other):
        return self.pos == other.pos

# Mapping is a numpy array, start_pt and end_pt are (x,y) coordinate tuples
def astar(mapping, start_pt, end_pt):
    width, height = mapping.shape

    start = Node(None, start_pt)
    end = Node(None, end_pt)

    open_list, closed_list = [], []
    open_list.append(start)

    while len(open_list) > 0:
        # Get the node with the smallest cost
        min_cost_node = open_list[0]
        min_idx = 0
        for idx, node in enumerate(open_list):
            if node.cost < min_cost_node.cost:
                min_cost_node = node
                min_idx = idx

        open_list.pop(min_idx)
        closed_list.append(min_cost_node)

        # Check to see if we've reached the end. If so backtrack through the path
        if min_cost_node.pos == end_pt:
            path = []
            node = min_cost_node
            while node is not None:
                path.append(node.pos)
                node = node.parent
            return path[::-1]

        # Go through neighbors. 
        neighbors = []
        for relative_direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_pos = (min_cost_node.pos[0] + relative_direction[0], min_cost_node.pos[1] + relative_direction[1])

            # Ignore if out of bounds
            if node_pos[0] > (width - 1) or node_pos[0] < 0 or node_pos[1] < 0 or node_pos[1] > (height - 1):
                continue
            # Avoid obstacles
            if mapping[node_pos[0]][node_pos[1]] != 0:
                continue

            new_node = Node(min_cost_node, node_pos)

            neighbors.append(new_node)

        for neighbor in neighbors:
            if neighbor in closed_list:
                continue

            neighbor.dist = min_cost_node.dist + 1
            # Calculate our heuristic as the sum of square distance
            neighbor.h = (neighbor.pos[0] - end_pt[0]) ** 2 + (neighbor.pos[1] - end_pt[1]) ** 2
            neighbor.cost = neighbor.dist + neighbor.h

            for op in open_list:
                if op == neighbor and op.dist < neighbor.dist:
                    continue

            open_list.append(neighbor)



def main():
    # map_fp = "working_map.npy"
    map_fp = "map.npy"
    maze = np.load(map_fp)

    start = (0, 120)
    end = (70, 180)

    path = astar(maze, start, end)

    map_path = maze.astype('float')
    for (y,x) in path:
        map_path[y,x] = 0.5
    cv2.imwrite('map_path.jpg',255*np.flip(map_path,axis=0))
    
    follow_path(start, path)

def follow_path(start,path):
    """Path: [(y,x)...]"""
    path.append((-10000,-10000)) #Sentinel node for end
    n = len(path)
    prev_dr = None
    dir_length = 0
    meta_path = []
    for i in range(1,n):
        dr = np.array(path[i]) - np.array(path[i-1])
        if (prev_dr == dr).all():
            dir_length+=1
        else:
            if prev_dr is not None:
                meta_path.append((tuple(prev_dr),norm(prev_dr)*dir_length))
            dir_length = 1
            prev_dr = dr
    print(meta_path)
    drive_meta_path(meta_path)

# Recognizable objects and their thresholds
DETECTABLES = {
    'stop sign': 0.3,
    'cell phone': 0.3,
    'person': 0.3
}

def drive_meta_path(path):
    theta_map = {
        (1,0):0,
        (1,-1):45,
        (0,-1):90,
        (-1,-1):135,
        (-1,0):180,
        (-1,1):-135,
        (0,1): -90,
        (1,1):-45,
    }
    prev_dir = 0
    for (direction,length) in path:
        direction = theta_map[direction]

        diff = direction - prev_dir
        if diff > 0:
            fc.turn_left(50)
        else:
            fc.turn_right(50)

        time.sleep(abs(diff) * 0.00833333)
        fc.stop()

        fc.forward(50)
        forward_while_camera(length * 0.02620922)
        fc.stop()
        prev_dir = direction

def forward_while_camera(duration):
    model, camera_id, width, height, num_threads, enable_edgetpu='efficientdet_lite0.tflite', 0, 640, 480,4, False
    options = ObjectDetectorOptions(
    num_threads=num_threads,
    score_threshold=0.3,
    max_results=3,
    enable_edgetpu=enable_edgetpu)
    detector = ObjectDetector(model_path=model, options=options)
    elapsed = 0
    while elapsed < duration:
        starttime = time.time()
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        image = cv2.flip(image, 1)

        # Run object detection estimation using the model.
        detected = False
        detections = detector.detect(image)
        for detection in detections:
            for category in detection.categories:
                threshold = DETECTABLES.get(category.label,100000)
                if category.score >= threshold:
                    detected = category.label
        dtime = time.time() - starttime
        if detected:
            fc.stop()
            print("Detected ", detected)
        else:
            fc.forward(50)
            print("Not detected")
            elapsed+=dtime

        cap.release()
        cap = None

if __name__ == '__main__':
    main()

