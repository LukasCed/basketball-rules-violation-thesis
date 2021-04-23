import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from Algorithm import Algorithm
from ImageProcessingUtils import print_img
    

vid = cv2.VideoCapture('images/hand_over_ball.jpg')
algorithm = Algorithm()

# Capture frame-by-frame
ret, frame = vid.read()
width = int(frame.shape[1] * 20 / 100)
height = int(frame.shape[0] * 20 / 100)
resized = cv2.resize(frame, (width, height), interpolation = cv2.INTER_AREA)

algorithm.execute(resized)

# Display the resulting frame
#print_img(frame)
key = cv2.waitKey(1) & 0xff

while True:

    key2 = cv2.waitKey(1) or 0xff

    if key2 == ord('p'):
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
vid.release()
cv2.destroyAllWindows()