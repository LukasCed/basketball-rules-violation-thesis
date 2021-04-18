# To use Inference Engine backend, specify location of plugins:
# export LD_LIBRARY_PATH=/opt/intel/deeplearning_deploymenttoolkit/deployment_tools/external/mklml_lnx/lib:$LD_LIBRARY_PATH
import cv2 as cv
import numpy as np
import argparse

class OpenPoseAlgorithm2:
    def __init__(this):
        protoFile = "C:/Users/Lukas/Desktop/BD/bachelor-thesis/program/op2/openpose_pose_mpi_faster_4_stages.prototxt"
        weightsFile = "C:/Users/Lukas/Desktop/BD/bachelor-thesis/program/op2/pose_iter_160000.caffemodel"

        this.net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)
        
    def execute(this, frame):

        BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                       "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                       "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                       "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }
        POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

        
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        
        frame = cv.resize(frame,(int(0.5*frameWidth), int(0.5*frameHeight)), interpolation = cv.INTER_CUBIC)

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        this.net.setInput(cv.dnn.blobFromImage(frame, 1.0 / 255, (frameWidth, frameHeight), (0, 0, 0), swapRB=False, crop=False))
        
        print("forwarding")
        out = this.net.forward()
        print("forwarded")

        H = out.shape[2]
        W = out.shape[3]
        # Empty list to store the detected keypoints
        points = []
        for i in range(len(out[0])):
            # confidence map of corresponding body's part.
            probMap = out[0, i, :, :]
            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv.minMaxLoc(probMap)
            # Scale the point to fit on the original image
            x = (frameWidth * point[0]) / W
            y = (frameHeight * point[1]) / H
            if prob > 0.6 :
                cv.circle(frame, (int(x), int(y)), 15, (0, 255, 255), thickness=-1, lineType=cv.FILLED)
                cv.putText(frame, "{}".format(i), (int(x), int(y)), cv.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, lineType=cv.LINE_AA)
                # Add the point to the list if the probability is greater than the threshold
                points.append((int(x), int(y)))
            else :
                points.append(None)

        cv.imshow('OpenPose using OpenCV', frame)
        return frame