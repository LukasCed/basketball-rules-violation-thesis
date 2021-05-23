from ImageProcessingUtils import *
import cv2
import numpy as np
import sys

lower_green = np.array([65, 10, 10])
upper_green = np.array([85, 230, 180])

lower_yellow_left = np.array([29,55,130])
upper_yellow_left = np.array([56,140,255])

lower_yellow_right = lower_yellow_left
upper_yellow_right = lower_yellow_left

lower_red1_left = np.array([0,120,100])
upper_red1_left = np.array([10,255,200])
lower_red2_left = np.array([170,120,100])
upper_red2_left = np.array([180,255,200])

lower_red1_right = lower_red1_left
upper_red1_right = upper_red1_left
lower_red2_right = lower_red2_left
upper_red2_right = upper_red2_left

class ColorBasedRecognitionAlgorithm:

    def __init__(this):
        pass
        
    def get_left_hand_mask(this, hsv):        
        return this.get_hand_mask(hsv, lower_yellow_left, upper_yellow_left)
        
    def get_right_hand_mask(this, hsv):        
        return this.get_hand_mask(hsv, lower_yellow_right, upper_yellow_right)

    def get_hand_mask(this, hsv, lower_yellow, upper_yellow):        
        mask_for_ball = segment_by_color(hsv, lower_green, upper_green)
        mask_for_ball = morph_dilate(morph_open(mask_for_ball))

        mask_for_hand = segment_by_color(hsv, lower_yellow, upper_yellow)
        mask_for_hand = morph_dilate(morph_open(mask_for_hand))
        
        # creating an inverted mask to segment out the ball from the rest of the frame
        mask_for_not_ball = cv2.bitwise_not(mask_for_ball)
        mask_for_hand = cv2.bitwise_and(mask_for_hand, mask_for_not_ball)
        
        mask_for_hand = dilate(erode(mask_for_hand, 3), 7)
        #cv2.imshow("mask for shoes", mask_for_shoes)
        return mask_for_hand

    def get_left_shoe_mask(this, hsv):
        return this.get_shoe_mask(hsv, lower_red1_left, upper_red1_left, lower_red2_left, upper_red2_left)
    
    def get_right_shoe_mask(this, hsv):
        return this.get_shoe_mask(hsv, lower_red1_right, upper_red1_right, lower_red2_right, upper_red2_right)
         
    def get_shoe_mask(this, hsv, color_range_min1, color_range_max1, color_range_min2, color_range_max2):
        mask_for_shoes1 = segment_by_color(hsv, color_range_min1, color_range_max1)
        mask_for_shoes2 = segment_by_color(hsv, color_range_min2, color_range_max2)
        mask_for_shoes = mask_for_shoes1 | mask_for_shoes2
        
        # optional optimisation: search for shoes only in lower part of frame
        height, width = mask_for_shoes.shape[:2]
        start_row, start_col = int(height * .4), int(0)
        end_row, end_col = int(height), int(width)
        mask_for_shoes = mask_for_shoes[start_row:end_row, start_col:end_col]
        
        mask_for_shoes = morph_dilate(morph_open(mask_for_shoes))
        mask_for_shoes = dilate(erode(mask_for_shoes, 6), 10)
        #cv2.imshow("mask for shoes", mask_for_shoes)
        return mask_for_shoes
    
    def get_ball_mask(this, hsv):
        mask_for_ball = segment_by_color(hsv, lower_green, upper_green)
        mask_for_ball = morph_dilate(morph_open(mask_for_ball))
        mask_for_ball = erode(dilate(erode(mask_for_ball, 100), 30), 3)
        #cv2.imshow("mask for shoes", mask_for_shoes)
        return mask_for_ball
        
    def preprocess(this, img):
        return img

