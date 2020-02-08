import cv2
import numpy as np 
from src.lego_finder import LegoFinder


class LegoMatcher:


    def __init__(self):
        self.blue = ([57, 50, 112], [131, 255, 255])
        self.yellow = ([14, 69, 164], [30, 255, 255])
        self.red = ([0, 43, 31], [12, 255, 255])
        self.grey = ([37, 3, 56], [110, 60, 153])
        self.white = ([37, 8, 177], [62, 50, 255])


    #masking image with given color
    def color_mask(self, image, color):
        imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, np.array(color[0]), np.array(color[1]))
        masked_image = cv2.bitwise_and(image, image, mask = mask)

        return masked_image


    def rectangle_condition(self, seperate_lego):
        number_of_objects = 0
       
        #height condition
        if seperate_lego.shape[0] > 85 and seperate_lego.shape[0] < 130:
            number_of_objects += 2

        elif seperate_lego.shape[0] > 130:
            number_of_objects += 3

        else:
            number_of_objects += 1

        # getting rid of noise 
        if np.count_nonzero(seperate_lego) < 1250:
            number_of_objects = 0
        
        return min(number_of_objects, 5)
            
            
    #returns dict with number for every color
    def get_colors_lego_number(self, image):
        masked = []
        numbers_detected = []
        masked.append(self.color_mask(image, self.red))
        masked.append(self.color_mask(image, self.blue))
        masked.append(self.color_mask(image, self.white))
        masked.append(self.color_mask(image, self.grey))
        masked.append(self.color_mask(image, self.yellow))
            
        for n, m in enumerate(masked):      
            if n == 2 or n == 3:
                numbers_detected.append(self.get_number_of_gwmasked(m))
            else:
                numbers_detected.append(self.get_number_of_masked(m))

        colors_with_numbers = {'red': numbers_detected[0], 'blue': numbers_detected[1], 
            'white': numbers_detected[2], 'grey': numbers_detected[3], 'yellow': numbers_detected[4]}
        
        return colors_with_numbers


    #another way for grey and white 
    def get_number_of_gwmasked(self, masked_image):
        gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3, 3), np.uint8)       
        erode = cv2.erode(gray, kernel, iterations = 2) #33)
        dilate = cv2.dilate(erode, kernel, iterations = 6)
        cnts, hierrarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ret, thresh = cv2.threshold(dilate, 40 ,255, cv2.THRESH_BINARY)
        counter = 0
        sep_lego = None
        for c in cnts:
            
            sep_lego = LegoFinder().crop_and_rot(thresh, c)#erode, c)
            counter += self.rectangle_condition(sep_lego)
        return counter        


    #returns number of specific color
    def get_number_of_masked(self, masked_image):
        gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        median = cv2.medianBlur(gray, 5)
        kernel = np.ones((3, 3), np.uint8)
        dilate = cv2.dilate(median, kernel, iterations = 6)
        erode = cv2.erode(dilate, kernel, iterations = 3) #33)
        cnts, hierrarchy = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ret, thresh = cv2.threshold(erode, 40 ,255, cv2.THRESH_BINARY)
        counter = 0
        sep_lego = None
        for c in cnts:
            
            sep_lego = LegoFinder().crop_and_rot(thresh, c)#erode, c)
            counter += self.rectangle_condition(sep_lego)            

        return counter


    def dict_compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return modified, same


    # to do: find better way to assign
    def assign(self, json_data, detect_list, name, number_of_holes):
        right_places = np.zeros((len(number_of_holes)), dtype = int)
        
        for m, d in enumerate(detect_list):   
            for n, j in enumerate(json_data[name]):
                if d == j:
                    right_places[n] = number_of_holes[m]
                    detect_list[m] = 0
        
        right_places, detect_list = self.assign_not_completed(4, detect_list, json_data, name, 
            number_of_holes, right_places)

        right_places, detect_list = self.assign_not_completed(3, detect_list, json_data, name, 
            number_of_holes, right_places)    
        
                 
        return right_places.tolist()


    #assign not matched with full completed
    def assign_not_completed(self, same_number, detect_list, json_data, name, number_of_holes, right_places):
        
        for number, not_assigned in enumerate(detect_list):
            if not_assigned != 0:
                for n, i in enumerate(right_places):
                    if i == 0:
                        modified, same = self.dict_compare(not_assigned, json_data[name][n])
                        if len(same) == same_number:
                            right_places[n] = number_of_holes[number]
                            detect_list[number] = 0  

        return right_places, detect_list


    def get_holes_in_right_order(self, images, json_data, json_labels):
        right_order_holes = []
        for n, image in enumerate(images):
            lego_bricks, number_of_holes  = LegoFinder().find_legos_holes(image)
            detect = []
            for l in lego_bricks:
                detect.append(LegoMatcher().get_colors_lego_number(l))
                
            right_order_holes.append(LegoMatcher().assign(json_data, 
                detect, json_labels[n], number_of_holes))
        
        return right_order_holes   
                    
                    

            
             

