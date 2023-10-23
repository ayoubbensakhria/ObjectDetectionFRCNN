import os
import glob
import argparse
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(xml_folder):
    xml_list = []
    for xml_file in glob.glob(os.path.join(xml_folder, '*.xml')):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        jpg_filename = root.find('filename').text
        for obj in root.findall('object'):
            obj_name = obj.find('name').text
            xmlbox = obj.find('bndbox')
            xmin = int(xmlbox.find('xmin').text)
            ymin = int(xmlbox.find('ymin').text)
            xmax = int(xmlbox.find('xmax').text)
            ymax = int(xmlbox.find('ymax').text)
            xml_list.append([jpg_filename, xmin, ymin, xmax, ymax, obj_name])
    column_names = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']
    xml_df = pd.DataFrame(xml_list, columns=column_names)
    return xml_df

def main(xml_folder, output_csv):
    xml_df = xml_to_csv(xml_folder)
    xml_df.to_csv(output_csv, index=None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_folder', required=True, help='Path to XML folder')
    parser.add_argument('--output_csv', required=True, help='Output CSV file path')
    args = parser.parse_args()
    main(args.xml_folder, args.output_csv)
