import cv2
from ImageProcessingUtils import *

class DoubleDribbleDetectionAlgorithm:

    def __init__(this):
        this.dribble_stopped = False
        this.in_hand_state = []
        this.in_hands = 0
        this.double_dribble = False
                          
    def execute(this, mask_for_ball, left_mask_for_hand, right_mask_for_hand, left_mask_for_shoe, right_mask_for_shoe):
    
        try:
            hand_and_ball = this.ball_in_hands(left_mask_for_hand | right_mask_for_hand, mask_for_ball)
            hand_and_ball_countours, h = find_contours(hand_and_ball)
            
            contour_count = len(hand_and_ball_countours)
                    
            if contour_count >= 1:
                this.in_hands = 1
            elif this.average_state(this.in_hand_state, 4) <= 0.3:
                this.in_hands = 0
            
            #checks if average state 10 frames back to now is less than 0.3, 0 indicating the ball wasnt in hands
            if this.dribble_stopped and this.in_hands == 1 and this.average_state(this.in_hand_state, 10) <= 0.3:
                this.double_dribble = True
            
            if contour_count >= 2 and not this.dribble_stopped and this.average_state(this.in_hand_state, 6) >= 1.2:
          #  if contour_count >= 2 and not this.dribble_stopped and this.average_state(this.in_hand_state, 5) >= 0.6:

                this.dribble_stopped = True
           
            this.in_hand_state.append(contour_count)

            #print("------------------------------")
            #print("ar double dribble", this.double_dribble)
            #print("dribble stopped", this.dribble_stopped)
            #print("contour count", contour_count)
            #print("avg state", this.average_state(this.in_hand_state, 10))
            #print("------------------------------")
            ##input()
        
        except BallNotFoundError as e:
              #print("Caught error when executing step rule violation algorithm ", repr(e))
              this.in_hands = 2
              
        except HandsNotFoundError as e:
              #print("Caught error when executing step rule violation algorithm ", repr(e))
              this.in_hands = 3
    
        return [this.in_hands, -1, this.double_dribble]
        
    # calculates avg state since n steps back
    def average_state(this, state, n):
        if len(state) == 0:
            return 0
        return sum(state[-n:]) / min(n, len(state))
        
    
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
        

class BallNotFoundError(Exception):
        pass
        
class HandsNotFoundError(Exception):
        pass