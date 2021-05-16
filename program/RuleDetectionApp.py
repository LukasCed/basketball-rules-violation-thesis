import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from ColorBasedRecognitionAlgorithm import ColorBasedRecognitionAlgorithm
from StepRuleViolationAlgorithm import StepRuleViolationAlgorithm
from ImageProcessingUtils import *
import time
import math

vid = cv2.VideoCapture('vids/test_inside_colors.mp4')

recognition_algorithm = ColorBasedRecognitionAlgorithm()
rule_violation_algorithm = StepRuleViolationAlgorithm()

ts1 = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    if frame is None:
        break
        
    orig_height, orig_width = frame.shape[:2]
    info_coord_start = (0, 0)
    info_coord_end = (math.floor(orig_width / 2), math.floor(orig_height / 5))
    
    #pre processing - prepare image
    img = flip_img(frame)
    hsv = convert_to_hsv(img)
    

    # get required masks (objects represented in boolean matric) from recognition algorithm
    hand_mask = recognition_algorithm.get_hand_mask(hsv)
    left_shoe_mask = recognition_algorithm.get_left_shoe_mask(hsv)
    right_shoe_mask = recognition_algorithm.get_right_shoe_mask(hsv)
    ball_mask = recognition_algorithm.get_ball_mask(hsv)
        
    state = rule_violation_algorithm.execute(ball_mask, hand_mask, left_shoe_mask, right_shoe_mask)
    
    in_hands = state[0]
    step_count = state[1]
    turnover = state[2]
    
    txt2 = "Zinsgniu skaicius: " + str(step_count)
    
    if in_hands == 3:
        txt = "Nesimato ranku"

    if in_hands == 2:
        txt = "Kamuolys nerastas"

    if in_hands == 1:
        txt = "Kamuolys rankose"
        
    if in_hands == 0:
        txt = "Kamuolys ne rankose"
        
    create_background(frame, info_coord_start, info_coord_end)
    put_text(frame, txt, (info_coord_start[0], info_coord_start[1] + math.ceil(info_coord_end[1] / 4)), font_size = 0.5 * (orig_height / 665))
    put_text(frame, txt2, (info_coord_start[0], info_coord_start[1] + 3 * math.ceil(info_coord_end[1] / 4)), font_size = 0.5 * (orig_height / 665))
    
    if turnover == True:
        put_text(frame, "Pazeista zingsniu taisykle!", (1000, 800), (0,0,255))
        put_text(frame, "Pazeista zingsniu taisykle!", (info_coord_start[0], info_coord_start[1] + 2 * math.ceil(info_coord_end[1] / 4)), font_size = 0.7 * (orig_height / 665), color = (0,0,255), font_thickness = math.ceil(2 * (orig_height / 665)))


    # Display the resulting frame
    #print_img(frame)
    cv2.imshow('frame', frame)

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