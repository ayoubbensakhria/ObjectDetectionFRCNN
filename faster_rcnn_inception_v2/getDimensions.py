import os
import glob #<- search files and folders in a path
import argparse
import xml.etree.ElementTree as ET
from matplotlib.pyplot import imread


def get_dimensions(path, extension="jpg"):
    """Iterates through all .jpg files in all subdirectories.

    Parameters:
    ----------
    path : {str}
        The path containing the .jpg files
    Returns
    -------
    two lists of heights and widths
    """
    # list of tuples containing heights and widths
    hw_pairs = []
    # list of classes with annotation count
    annotation_count = {}
    # Search recursively in subdirectories
    for jpg_file in glob.glob(path + '/**/*.{ext}'.format(ext=extension), recursive=True):
        try:
            # get current folder
            current_folder = os.path.basename(os.path.dirname(jpg_file))
            # Exclude train, test, valid
            if current_folder in ['train', 'test', 'valid']:
                continue
            img = imread(jpg_file)
            # check if xml with the same filename exists
            xml_filename = os.path.splitext(jpg_file)[0] + '.xml'
            annotated = 1 if os.path.exists(xml_filename) else 0
            # get height and width
            height, width, _ = img.shape
            # update annotation count
            if current_folder in annotation_count:
                annotation_count[current_folder] += annotated
            else:
                annotation_count[current_folder] = annotated
            # check class
            if height is not None and width is not None:
                hw_pairs.append((height,width))
            else:
                continue
        except:
            print('An arror occured with the file:', jpeg_file)
            continue
    print(hw_pairs) # <- index 0
    print (annotation_count) # <- index 1


def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Get Image Dimensions")
    parser.add_argument("-i",
                        "--inputDir",
                        help="Root path to the folder where the input image files are stored",
                        type=str)
    parser.add_argument("-ex",
                        "--extension",
                        help="Image extension",
                        default="jpg",
                        type=str)
    args = parser.parse_args()

    if(args.inputDir is None):
        args.inputDir = os.getcwd()

    assert(os.path.isdir(args.inputDir))
    get_dimensions(args.inputDir, args.extension)

if __name__ == '__main__':
    main()
