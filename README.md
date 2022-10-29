# Basketball Rule Violation Detection

This is a project for basketball rules violation recognition that I did for my bachelor thesis. 

The video parsing algorithm parses specific body parts (hands, ankles etc), and forwards the matrices which encode the location of relevant body parts to rule violation detection algorithm.

#### The rule violation detection algorithm: ####

1) Detects whether the ball is the hands or not
2) If ball is in hands:
    1) Count steps using step counting algorithm
    2) If 3 or more steps counted, return rule violation 
4) The ball is not in hands - step count is set to 0 

#### The step counting algorithm: ####

The intuition of the algorithm: 
Observe how a person (who has two functional legs) walks, paying attention only to the legs (or feet/ankles/shoes). At most moments, looking from the side, we can count two feet. However, as legs are crossing each other, for a short moment the leg that is closer to us "hides" the other feet, where we'd count only one foot. 

The algorithm uses this idea - it keeps count of the feet countours and, as there is a switch from 2 to 1, a step is increased.

#### Basketball-in-hands detection algorithm: ####

Similar idea to step counting algorithm. First, we parse the ball the hands from the image. Then, we perform element-wise AND operation on matrices (that represent the frames that contain the objects). Consider the frames where the ball is in the hands - hands overlap with the ball and thus element-wise AND operation will return a matrix that will necessarely contain some amount of 1's. If that amount is above a certain threshold, we assume the ball is in the hands. 

### How to install and run the app: ###

1) Install conda
2) cd into program folder 
3) Enter "conda env create" to create an environment from environment.yml
4) Enter "conda activate pytorch1" to activate the environment that was created
5) Add videos to program/vids folder, reference them in the code of app file you want to use
6) Run "python ViolationDetectionApp.py" to execute the main program


### How to run the tests: ###
1) After completing installation steps, run "python TestSuite.py". Might need to change the assertions according to which videos you're testing.

### References ###

I used [Lightweight OpenPose](https://github.com/Daniil-Osokin/lightweight-human-pose-estimation.pytorch) to detect body parts in video frames
