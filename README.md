# Lego_holes_finder
Finding holes in lego bricks with OpenCV. Also mathcing numbers of bricks for every color. 

## Requirements
'''
pip3 install -r requirements.txt
'''

## Running script 
When running script, there is need to pass 3 arguments:
* IMAGES_PATH - absolute path to folder with bricks images
* INPUT_FILE_PATH - absolute path to input json file, which includes bricks description
* OUTPUT_FILE_PATH - absolute path to output json file with results

'''
python3 main.py IMAGES_PATH  INPUT_FILE_PATH OUTPUT_FILE_PATH
'''

## Testing
To check the results run thew test.py script with 3 arguments:
* INPUT_FILE_PATH - absolute path to input json file, which includes bricks description
* EXPECTED_OUTPUT_FILE_PATH absolut path to json file, which includes expected output results
* OUTPUT_FILE_PATH - absolute path to output json file with results, which was saved with main script

'''
python3 test.py INPUT_FILE_PATH EXPECTED_OUTPUT_FILE_PATH OUTPUT_FILE_PATH
'''

Test script prints out when there are differences between output file and expected output file. It also prints score. 
