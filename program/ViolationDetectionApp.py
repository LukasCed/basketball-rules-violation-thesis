import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
#from ColorBasedRecognitionAlgorithm import ColorBasedRecognitionAlgorithm
from NeuralNetworkRecognitionAlgorithm import NeuralNetworkRecognitionAlgorithm
from TravelDetectionAlgorithm import TravelDetectionAlgorithm
from DoubleDribbleDetectionAlgorithm import DoubleDribbleDetectionAlgorithm
from ImageProcessingUtils import *
import time
import math

vid = cv2.VideoCapture('vids/videos/double_dribble_9.mp4')

# recognition_algorithm = ColorBasedRecognitionAlgorithm()
recognition_algorithm = NeuralNetworkRecognitionAlgorithm()

rule_violation_algorithms = [TravelDetectionAlgorithm(), DoubleDribbleDetectionAlgorithm()]
rule_violations = ["Travelling violation", "Double dribble violation"]

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
    img = recognition_algorithm.preprocess(img)
    hsv = convert_to_hsv(img)
    
    #initialize
    in_hands = -1
    step_count = -1
    violation_text = ""
    turnover = False
    
    # get required masks (objects represented in boolean matric) from recognition algorithm
    left_hand_mask = recognition_algorithm.get_left_hand_mask(hsv)
    right_hand_mask = recognition_algorithm.get_right_hand_mask(hsv)
    
    left_shoe_mask = recognition_algorithm.get_left_shoe_mask(hsv)
    right_shoe_mask = recognition_algorithm.get_right_shoe_mask(hsv)
    
    ball_mask = recognition_algorithm.get_ball_mask(hsv)
    
    ##cv2.namedWindow('left_hand', cv2.WINDOW_NORMAL)
    ##cv2.namedWindow('right_hand', cv2.WINDOW_NORMAL)
    #cv2.namedWindow('left_shoe_mask', cv2.WINDOW_NORMAL)
    #cv2.namedWindow('ball_mask', cv2.WINDOW_NORMAL)
    ##cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    ##cv2.imshow("left_hand", (left_hand_mask | right_hand_mask) | ball_mask)
    ##cv2.imshow("right_hand", (left_shoe_mask | right_shoe_mask))

    #cv2.imshow("left_shoe_mask", left_shoe_mask | right_shoe_mask)
    
    #cv2.imshow("ball_mask", ball_mask)
    #input()
       
    for i, algorithm in enumerate(rule_violation_algorithms):
        
        # 0 in hands - 0 no, 1 yes, 2 bal not found, 3 hands not found
        # 1 step count - 0 - inf. -1 - no information
        # 2 turnover - true/false
        state = algorithm.execute(ball_mask.copy(), left_hand_mask.copy(), right_hand_mask.copy(), left_shoe_mask.copy(), right_shoe_mask.copy())
        
        if in_hands == -1:
            in_hands = state[0]
            
        if step_count == -1:
            step_count = state[1]
            
        if turnover == False:
            turnover = state[2]
        
        if violation_text == "" and turnover:
            violation_text = rule_violations[i]
    
    txt2 = "Zinsgniu skaicius: " + str(step_count)
    
    if in_hands == 3:
        txt = "Nesimato zaidejo ranku"

    if in_hands == 2:
        txt = "Kamuolys nerastas"

    if in_hands == 1:
        txt = "Kamuolys rankose"
        
    if in_hands == 0:
        txt = "Kamuolys ne rankose"
                
    create_background(frame, info_coord_start, info_coord_end)
    put_text(frame, txt, (info_coord_start[0], info_coord_start[1] + math.ceil(info_coord_end[1] / 4)), font_size = 0.5 * (orig_height / 665))
    put_text(frame, txt2, (info_coord_start[0], info_coord_start[1] + 3 * math.ceil(info_coord_end[1] / 4)), font_size = 0.5 * (orig_height / 665))
    
    # todo: instead zingsniu, variable
    if turnover == True:
        put_text(frame, violation_text, (info_coord_start[0], info_coord_start[1] + 2 * math.ceil(info_coord_end[1] / 4)), font_size = 0.7 * (orig_height / 665), color = (0,0,255), font_thickness = math.ceil(2 * (orig_height / 665)))


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