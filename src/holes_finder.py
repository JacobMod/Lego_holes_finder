import cv2
import numpy as np 


class HolesFinder:

    #finding holes on single object
    def find_holes(self, found_object):
        in_gray_object = cv2.cvtColor(found_object, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(in_gray_object,cv2.HOUGH_GRADIENT, 1, 35,
                            param1=43, param2=18, minRadius=4, maxRadius=16)
        circle_counter = 0
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                circle_counter += 1
                
        return circles, circle_counter
    

