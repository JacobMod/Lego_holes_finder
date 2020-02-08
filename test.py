import argparse
from src.json_handler import *

ap = argparse.ArgumentParser()

ap.add_argument('input_file', action = 'store')
ap.add_argument('expected_output_file', action = 'store')
ap.add_argument('output_directory', action = 'store')
args = vars(ap.parse_args())


def evaluate():
    descriptions = json.load(open(args['input_file']))
    expected = JsonHandler().load_json(args['expected_output_file'])
    result = JsonHandler().load_json(args['output_directory'])

    score = 0.0
    diff_sum = 0.0
    gt_sum = 0.0

    for (img_name, _), (_, sheet) in zip(descriptions.items(), result.items()):
        for exp, res in zip(expected[img_name], sheet):
            diff = abs(exp - res)
            if diff != 0:
                print(f'Error at image {img_name} of value: {diff}. '
                      f'Expected {exp} but got {res}')
            diff_sum += diff
            gt_sum += exp
        score += diff_sum / gt_sum

    print('Score:', score / len(descriptions.items()))


evaluate()