import cv2
import numpy as np
import glob


class ImageHandler():


    def get_imgs(self, imgs_path):
        imgs_path +=  '/*.jpg'
        imgs = [cv2.imread(img) for img in sorted(glob.glob(imgs_path))]

        return imgs

    
    def image_resize(self, scale, images):
        scale_percent = scale
        width = int(images[0].shape[1] * scale_percent / 100)
        height = int(images[0].shape[0] * scale_percent / 100)
        dim = (width, height)
        for i in range(len(images)):
            images[i] = cv2.resize(images[i], dim, interpolation = cv2.INTER_AREA)

        return images

    #show finded objects, when saved
    def show_single_object(self):
        curr_img = 0
        warp_image = [cv2.imread(img) for img in sorted(glob.glob('*.png'))]

        while True:
            cv2.imshow('Image', warp_image[curr_img])
            k = cv2.waitKey(1) & 0xFF

            if k == ord('q'):
                break

            elif k == ord('w'):
                if curr_img == 0:
                    curr_img = len(warp_image) - 1
                else:
                    curr_img -= 1

            elif k == ord('e'):
                if curr_img == len(warp_image) - 1:
                    curr_img = 0
                else:
                    curr_img += 1

        cv2.destroyAllWindows()