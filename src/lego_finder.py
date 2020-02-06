from src.holes_finder import *
from scipy.spatial import distance as dist


class LegoFinder:


    #get points in order to have good rotate
    def order_points(self, pts):
        x_sorted = pts[np.argsort(pts[:, 0]), :]
        left_most = x_sorted[:2, :]
        right_most = x_sorted[2:, :]
        left_most = left_most[np.argsort(left_most[:, 1]), :]
        (tl, bl) = left_most
        D = dist.cdist(tl[np.newaxis], right_most, "euclidean")[0]
        (br, tr) = right_most[np.argsort(D)[::-1], :]

        return np.array([tl, tr, br, bl], dtype = "float32")


    #crop to single object from whole image and rotate
    def crop_and_rot(self, img, contour):
        rect = cv2.minAreaRect(contour)
        angle = rect[2]
        box = cv2.boxPoints(rect)
        box = self.order_points(box)
        width = np.int(np.linalg.norm([box[0, 0] - box[1, 0], box[0, 1] - box[1, 1]]))
        height = np.int(np.linalg.norm([box[0, 0] - box[-1, 0], box[0, 1] - box[-1, 1]]))
        src_pts = box.astype(np.float32)
        dst_pts = np.array([[0, 0],
                            [width - 1, 0],
                            [width - 1, height - 1],
                            [0, height - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(img, M, (width, height), None, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT,
                                     (255, 255, 255))
        
        if warped.shape[0] > warped.shape[1]:
            warped = cv2.rotate(warped, cv2.ROTATE_90_COUNTERCLOCKWISE)

        return warped


    #find objects on given image
    def find_objects(self, image):
        warped_imgs = []
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        median = cv2.medianBlur(gray_img, 5)
        canny = cv2.Canny(gray_img, 60, 255, 1)
        kernel = np.ones((7, 7),np.uint8)
        dilate = cv2.dilate(canny, kernel, iterations=10)
        erode = cv2.erode(dilate, kernel, iterations=4)
        cnts, hierrarchy = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            warped_imgs.append(self.crop_and_rot(image, c))

        return warped_imgs
        

    #get lego holes and number of them
    def find_legos_holes(self, image):

            legos = self.find_objects(image)
            right_legos = []
            number_of_holes = []

            for m, lego in enumerate(legos):
                circles, circle_counter = HolesFinder().find_holes(lego)
                if circle_counter > 0:
                    right_legos.append(lego)
                    number_of_holes.append(circle_counter)
            
            return right_legos, number_of_holes 

    
    def save_lego_images(self, legos, number_of_image):
        print('IMAGE: ', number_of_image)    
        for m, lego in enumerate(legos): 
        
            file_name = 'object' + str(number_of_image + 1) + '_' + str(m + 1) + '.png'
            cv2.imwrite(file_name, lego)


                
