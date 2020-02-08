import argparse 
from src.lego_finder import *
from src.json_handler import JsonHandler
from src.lego_matcher import LegoMatcher
from src.image_handler import *


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument('img_path', action = 'store')
    ap.add_argument('input_json', action = 'store')
    ap.add_argument('output_json', action = 'store')
    args = vars(ap.parse_args())

    images = ImageHandler().get_imgs(args['img_path'])
    images = ImageHandler().image_resize(50, images)

    json_data = JsonHandler().load_json(args['input_json'])
    json_data = JsonHandler().change_values_to_int(json_data)
    json_labels = JsonHandler().get_data_names(json_data)

    right_order_holes = LegoMatcher().get_holes_in_right_order(images, json_data, json_labels)

    JsonHandler().write_json(args['output_json'], json_labels, right_order_holes)


if __name__ == '__main__':
    main()

    
    


