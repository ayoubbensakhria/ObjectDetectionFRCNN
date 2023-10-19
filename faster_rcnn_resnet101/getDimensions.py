import os
import glob
import argparse
import xml.etree.ElementTree as ET
from matplotlib.pyplot import imread

def get_dimensions(path, extension="jpg"):
    hw_pairs = []
    annotation_count = {}
    for xml_file in glob.glob(path + '/**/*.xml', recursive=True):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            width = int(root.find('.//size/width').text)
            height = int(root.find('.//size/height').text)
            hw_pairs.append((height, width))
            
            current_class = root.find('.//object/name').text
            if current_class in annotation_count:
                annotation_count[current_class] += 1
            else:
                annotation_count[current_class] = 1
        except Exception as e:
            print(f'An error occurred with the file: {xml_file}. Error: {e}')
            continue

    print(hw_pairs)
    print(annotation_count)

def main():
    parser = argparse.ArgumentParser(description="Get Image Dimensions")
    parser.add_argument("-i", "--inputDir", help="Root path to the folder where the input image files are stored", type=str)
    parser.add_argument("-ex", "--extension", help="Image extension", default="jpg", type=str)
    args = parser.parse_args()

    if(args.inputDir is None):
        args.inputDir = os.getcwd()

    assert(os.path.isdir(args.inputDir))
    get_dimensions(args.inputDir, args.extension)

if __name__ == '__main__':
    main()
