from ImageProcessingUtils import *
import cv2
import numpy as np
import sys
sys.path.append('./lightweighthpe')
from lightweighthpe.app import *

left_hand_color_range = np.array([60, 255, 255]) #green
right_hand_color_range = np.array([60, 255, 127])

left_leg_color_range = np.array([0, 255, 255]) #red
right_leg_color_range = np.array([0, 255, 127])

lower_green = np.array([65, 80, 38])
upper_green = np.array([84, 240, 255])

class NeuralNetworkRecognitionAlgorithm:

    def __init__(this, cpu = False):
        this.net = this.setup_lightweight(cpu)
        this.cpu = cpu
        
    def get_left_hand_mask(this, hsv):        
        return this.get_hand_mask(hsv, left_hand_color_range, left_hand_color_range)
        
    def get_right_hand_mask(this, hsv):        
        return this.get_hand_mask(hsv, right_hand_color_range, right_hand_color_range)

    def get_hand_mask(this, hsv, color_range_min, color_range_max):        
        # mask_for_ball = segment_by_color(hsv, color_range_min, color_range_max) - not sure what is this for anymore
        # creating an inverted mask to segment out the ball from the rest of the frame
        # mask_for_not_ball = cv2.bitwise_not(mask_for_ball)
        #mask_for_hand = cv2.bitwise_and(mask_for_hand, mask_for_not_ball)
        
        mask_for_hand = segment_by_color(hsv, color_range_min, color_range_max)

        #cv2.imshow("mask for hand" +  np.array2string(color_range_min), mask_for_hand)
        return mask_for_hand

    def get_left_shoe_mask(this, hsv):
        return this.get_shoe_mask(hsv, left_leg_color_range, left_leg_color_range)
    
    def get_right_shoe_mask(this, hsv):
        return this.get_shoe_mask(hsv, right_leg_color_range, right_leg_color_range)
         
    def get_shoe_mask(this, hsv, color_range_min, color_range_max):
        mask_for_shoes = segment_by_color(hsv, color_range_min, color_range_max)
        #cv2.imshow("mask for shoes" + np.array2string(color_range_min), mask_for_shoes)
        return mask_for_shoes
    
    def get_ball_mask(this, hsv):
        mask_for_ball = segment_by_color(hsv, lower_green, upper_green)
        mask_for_ball = morph_dilate(morph_open(mask_for_ball))
        mask_for_ball = erode(dilate(mask_for_ball, 15), 3)
        #cv2.imshow("mask_for_ball", mask_for_ball)
        return mask_for_ball
        
    def setup_lightweight(this, cpu): 
        net = PoseEstimationWithMobileNet()
        checkpoint = torch.load("./lightweighthpe/checkpoint_iter_370000.pth", map_location='cpu')
        load_state(net, checkpoint)     
        net = setup(net, cpu)
        return net
        
    def preprocess(this, img):
        return run_lightweight(this.net, img, cpu = this.cpu)

