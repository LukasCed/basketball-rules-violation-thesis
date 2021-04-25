import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from Algorithm import Algorithm
from ImageProcessingUtils import print_img
import time

vid = cv2.VideoCapture('vids/2.mp4')
algorithm = Algorithm()
ts1 = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    if frame is None:
        break

    frame = algorithm.execute(frame)

    # Display the resulting frame
    print_img(frame)
    key = cv2.waitKey(1) & 0xff

    if key == ord('p'):

        while True:

            key2 = cv2.waitKey(1) or 0xff
            cv2.imshow('frame', frame)

            if key2 == ord('p'):
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

ts2 = time.time()
print("time taken ms", (ts2 - ts1) * 1000)
# When everything done, release the capture
vid.release()
cv2.destroyAllWindows()