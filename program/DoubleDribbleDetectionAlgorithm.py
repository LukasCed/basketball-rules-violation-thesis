import cv2
from ImageProcessingUtils import *

class DoubleDribbleDetectionAlgorithm:

    def __init__(this):
        this.dribble_stopped = False
        this.in_hand_state = []
        this.in_hands = 0
        this.double_dribble = False
                          
    def execute(this, mask_for_ball, left_mask_for_hand, right_mask_for_hand, left_mask_for_shoe, right_mask_for_shoe):
    
        hand_and_ball = (mask_for_ball & right_mask_for_hand) | (mask_for_ball & left_mask_for_hand)
        hand_and_ball_countours, h = find_contours(hand_and_ball)
        
        contour_count = len(hand_and_ball_countours)
                
        if contour_count >= 1:
            this.in_hands = 1
        elif this.average_state(this.in_hand_state, 4) <= 0.3:
            this.in_hands = 0
        
        #checks if average state 10 frames back to now is less than 0.3, 0 indicating the ball wasnt in hands
        if this.dribble_stopped and this.in_hands == 1 and this.average_state(this.in_hand_state, 10) <= 0.3:
            this.double_dribble = True
        
        if contour_count >= 2 and not this.dribble_stopped and this.average_state(this.in_hand_state, 5) >= 0.6:
            this.dribble_stopped = True
       
        this.in_hand_state.append(contour_count)

        #print("ar double dribble", this.double_dribble)
        #print("dribble stopped", this.dribble_stopped)
        #print("contour count", contour_count)
        #print("avg state", this.average_state(this.in_hand_state, 10))
        
        return [this.in_hands, -1, this.double_dribble]
        
    # calculates avg state since n steps back
    def average_state(this, state, n):
        if len(state) == 0:
            return 0
        return sum(state[-n:]) / min(n, len(state))
    