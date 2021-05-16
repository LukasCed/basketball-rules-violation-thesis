import cv2
from ImageProcessingUtils import *

class TravelDetectionAlgorithm:
    # find out if ball is in hands
    ## needs: mask for ball, mask for hands
    # calculate steps
    ## needs: mask for shoes

    def __init__(this):
        this.feet_intersection = False
        this.step_count = 0
        this.turnover = False
        this.in_hand_state = []
        this.in_hands = 0
        
    # returns a list [x,y,z]
    # x - whether the ball is in hands. 1 - true, 0 false, 2 - ball not found, 3 - hands not found
    # y - step count (0 to inf.)
    # z - whether it's turnover. true, false
    def execute(this, mask_for_ball, left_mask_for_hand, right_mask_for_hand, left_mask_for_shoe, right_mask_for_shoe):
    
        mask_for_hand = left_mask_for_hand | right_mask_for_hand        
        
        try:
            hand_and_ball = this.ball_in_hands(mask_for_hand, mask_for_ball)
            hand_and_ball_countours, h = find_contours(hand_and_ball)
            contour_count = len(hand_and_ball_countours)
        
            this.in_hand_state.append(contour_count)

            pixel_pctg = hand_and_ball[np.where(hand_and_ball >= 1)].size / hand_and_ball.size * 100
            
            if this.average_state(this.in_hand_state, 10) >= 0.6: 
            # if pixel_pctg > 0.001 and this.average_state(this.in_hand_state, 4) >= 0.5:  (palyginti percentages)
                this.in_hands = 1
                this.calculate_steps(left_mask_for_shoe, right_mask_for_shoe)
                this.compute_turnover()
            elif this.average_state(this.in_hand_state, 5) <= 0.3: # trying to make sure it has been out of hands for more than five frames
                this.step_count = 0 # step counting not relevant when ball is not in hands
                this.in_hands = 0

        except BallNotFoundError as e:
              #print("Caught error when executing step rule violation algorithm ", repr(e))
              this.in_hands = 2
              
        except HandsNotFoundError as e:
              #print("Caught error when executing step rule violation algorithm ", repr(e))
              this.in_hands = 3
    
        return [this.in_hands, this.step_count, this.turnover]


    def ball_in_hands(this, mask_for_hand, mask_for_ball):
        ball_contours, h = find_contours(mask_for_ball)
        hand_contours, h = find_contours(mask_for_hand)
        if len(hand_contours) < 1:
            raise HandsNotFoundError("No hand contours found")
                    
        ball_contour = choose_largest_contours(ball_contours)
        
        if ball_contour is not None:
            (x,y),radius = cv2.minEnclosingCircle(ball_contour)
            center = (int(x),int(y))
            cv2.circle(mask_for_ball,center,int(radius),(255,0,0), -1)
            
            # for drawing ball contours
            #_, bc, h = find_contours(mask_for_ball)
            #cv2.drawContours(img, bc, -1, (0,255,0), 3)

            # fill hand
            cv2.fillPoly(mask_for_hand, color = (255, 0, 0), pts = hand_contours )

            hand_and_ball = cv2.bitwise_and(mask_for_ball,mask_for_ball,mask=mask_for_hand)
            hand_and_ball = np.array(hand_and_ball)
            return hand_and_ball
        
        else:
            raise BallNotFoundError("No ball contours found")

        return []  

    
    def calculate_steps(this, mask_for_shoes_left, mask_for_shoes_right):
        shoe_contours, h = find_contours(mask_for_shoes_left | mask_for_shoes_right)
        any_empty = np.all(mask_for_shoes_left == 0) or np.all(mask_for_shoes_right == 0)
                
        if len(shoe_contours) == 1 and not this.feet_intersection and not any_empty:
            this.feet_intersection = True
            this.step_count = this.step_count + 1

        elif len(shoe_contours) > 1:
            this.feet_intersection = False
            
    def compute_turnover(this):
        if this.step_count > 2:
            this.turnover = True
            
  # calculates avg state since n steps back
    def average_state(this, state, n):
        if len(state) == 0:
            return 0
        return sum(state[-n:]) / min(n, len(state))
    
  
class BallNotFoundError(Exception):
        pass
        
class HandsNotFoundError(Exception):
        pass