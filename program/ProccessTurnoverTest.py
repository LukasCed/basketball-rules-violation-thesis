import numpy as np
import cv2
from PIL import Image
from NeuralNetworkRecognitionAlgorithm import NeuralNetworkRecognitionAlgorithm
from TravelDetectionAlgorithm import TravelDetectionAlgorithm
from DoubleDribbleDetectionAlgorithm import DoubleDribbleDetectionAlgorithm
from ImageProcessingUtils import *

def proccess_turnover_test(video_path):

    vid = cv2.VideoCapture(video_path)
    recognition_algorithm = NeuralNetworkRecognitionAlgorithm()
    rule_violation_algorithms = [TravelDetectionAlgorithm(), DoubleDribbleDetectionAlgorithm()]
    rule_violations = ["Travelling violation", "Double dribble violation"]
    
    ret, frame = vid.read()
    turnover = False
    index = -1

    while(not turnover and not frame is None):
        #pre processing - prepare image
        img = flip_img(frame)
        img = recognition_algorithm.preprocess(img)
        hsv = convert_to_hsv(img)
        
        left_hand_mask = recognition_algorithm.get_left_hand_mask(hsv)
        right_hand_mask = recognition_algorithm.get_right_hand_mask(hsv)
    
        left_shoe_mask = recognition_algorithm.get_left_shoe_mask(hsv)
        right_shoe_mask = recognition_algorithm.get_right_shoe_mask(hsv)
    
        ball_mask = recognition_algorithm.get_ball_mask(hsv)

        for i, algorithm in enumerate(rule_violation_algorithms):
        
        # 0 in hands - 0 no, 1 yes, 2 bal not found, 3 hands not found
        # 1 step count - 0 - inf. -1 - no information
        # 2 turnover - true/false
            state = algorithm.execute(ball_mask, left_hand_mask, right_hand_mask, left_shoe_mask, right_shoe_mask)
            if turnover == False:
                turnover = state[2]
                index = i

        
        ret, frame = vid.read()



    # When everything done, release the capture
    vid.release()
    cv2.destroyAllWindows()
    print("video", video_path, "is done processing")
    return (turnover, index)