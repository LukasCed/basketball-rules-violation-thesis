import cv2
import numpy as np

green_lower = np.uint8([[[37,53,14 ]]])
green_higher = np.uint8([[[100,114,49 ]]])

yellow_lower = np.uint8([[[111,157,117 ]]])
yellow_higher = np.uint8([[[151,227,230 ]]])

red_lower = np.uint8([[[27,11,124 ]]])
red_higher = np.uint8([[[77,58,180 ]]])

red = np.uint8([[[160,160,190 ]]])


hsv_green_lower = cv2.cvtColor(green_lower,cv2.COLOR_BGR2HSV)
hsv_green_higher = cv2.cvtColor(green_higher,cv2.COLOR_BGR2HSV)

hsv_yellow_lower = cv2.cvtColor(yellow_lower,cv2.COLOR_BGR2HSV)
hsv_yellow_higher = cv2.cvtColor(yellow_higher,cv2.COLOR_BGR2HSV)

hsv_red_lower = cv2.cvtColor(red_lower,cv2.COLOR_BGR2HSV)
hsv_red_higher = cv2.cvtColor(red_higher,cv2.COLOR_BGR2HSV)

hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)

print("green")
print(hsv_green_lower)
print(hsv_green_higher)

print("yellow")
print(hsv_yellow_lower)
print(hsv_yellow_higher)

print("red")
print(hsv_red_lower)
print(hsv_red_higher)
print(hsv_red)
