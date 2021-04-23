import cv2
from matplotlib import pyplot as plt
import numpy as np

vid = cv2.VideoCapture('dribble.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=50, minRadius=30, maxRadius=500)
    if circles is not None:
        for x, y, r in circles[0]:
            c = plt.Circle((x, y), r, fill=False, lw=3, ec='C1')
            plt.gca().add_patch(c)
    plt.gcf().set_size_inches((12, 8))
    plt.show()

# When everything done, release the capture
vid.release()
cv2.destroyAllWindows()
