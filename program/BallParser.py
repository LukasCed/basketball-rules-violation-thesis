import cv2
from matplotlib import pyplot as plt
import numpy as np
from skimage.transform import hough_ellipse
from skimage.feature import canny

vid = cv2.VideoCapture('vids/ball_img_2_small.jpg')

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=50, minRadius=30, maxRadius=500)

    edges = canny(img, sigma=3.0)
    
    for edge in edges:
        plt.plot(edge[1], edge[0], linewidth=2)
    plt.imshow(edges, cmap='gray')
    plt.show()
    print(edges)
    print("pries elipses")

    ellipses = hough_ellipse(edges, accuracy=20, threshold=500,
                       min_size=50, max_size=200)
    print("daejo iki elipsiu")

    if circles is not None:
        for x, y, r in circles[0]:
            c = plt.Circle((x, y), r, fill=False, lw=3, ec='C1')
            plt.gca().add_patch(c)
            
    if ellipses is not None:
        for x, y, r in ellipses[0]:
            c = plt.Ellipse((x, y), r, fill=False, lw=3, ec='C1')
            plt.gca().add_patch(c)
            
    plt.gcf().set_size_inches((12, 8))
    plt.show()

# When everything done, release the capture
vid.release()
cv2.destroyAllWindows()
