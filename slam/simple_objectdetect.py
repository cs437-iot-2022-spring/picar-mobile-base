# from picar_4wd import us
# from picar_4wd import servo
import picar_4wd as fc

import random
import signal
import sys
import argparse
import sys
import time

import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils


# Threshold distance to wall. In cm
THRESHOLD = 20

# How many loop iterations to turn for. 
TURN_DURATION = 500

# Recognizable objects and their thresholds
DETECTABLES = {
    'stop sign': 0.3,
    'cell phone': 0.3,
    'person': 0.3
}

#Interrupt handler
def signal_handler(signal, frame):
    fc.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def run(model: str, camera_id: int, width: int, height: int, num_threads: int, enable_edgetpu: bool) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """
    # Object detection initialization
    counter, fps = 0, 0
    start_time = time.time()
    # cap = cv2.VideoCapture(camera_id)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    options = ObjectDetectorOptions(
        num_threads=num_threads,
        score_threshold=0.3,
        max_results=3,
        enable_edgetpu=enable_edgetpu)
    detector = ObjectDetector(model_path=model, options=options)
    while True:
        print("FPS ",1/(time.time()-start_time))
        start_time = time.time()
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        counter += 1
        image = cv2.flip(image, 1)

        # Run object detection estimation using the model.
        detected = False
        detections = detector.detect(image)
        for detection in detections:
            for category in detection.categories:
                threshold = DETECTABLES.get(category.label,100000)
                if category.score >= threshold:
                    detected = category.label

        if detected:
            fc.stop()
            print("Detected ",detected)
        else:
            fc.forward(1)
            # print("GO")


        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break
        cap.release()
        cap = None

if __name__ == '__main__':
    run('efficientdet_lite0.tflite', 0, 640, 480,4, False)



