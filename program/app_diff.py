import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from Algorithm import Algorithm
from ImageProcessingUtils import print_img
import time
    
ts1 = time.time()

vid = cv2.VideoCapture('vids/6.mp4')
algorithm = Algorithm()
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
prev = None

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

made = 0
steps = 0
plot_data = []

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    frame = fgbg.apply(frame)
    
    made, steps = algorithm.execute_diff(prev, frame, made, steps, plot_data)
    if frame is not None:
        prev = frame.copy()
    else:
        break
    
    print(steps)

    # Display the resulting frame
    #print_img(frame)
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
#x = [list(t) for t in zip(*plot_data)]
#print(x)
plt.plot(x[0], x[1])
plt.plot(x[0], [0.1] * len(x[0]))
plt.plot(x[0], [0.5] * len(x[0]))
plt.ylabel("Aktyvių pikselių kiekis procentais")
plt.xlabel("Kadro nr.")
plt.show()
input()
cv2.destroyAllWindows()