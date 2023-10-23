import os
import io
import pandas as pd
import tensorflow as tf
from PIL import Image
import argparse
from object_detection.utils import dataset_util

def class_text_to_int(row_label):
    class_mapping = {
        "indian_robinrotation": 1,
        "oriental_magpie_robinrotation": 2,
        "alexandrine_parakeetrotation": 3,
        "asian_koelrotation": 4,
        "indian_paradise-flycatcherrotation": 5,
        "laughing_doverotation": 6,
        "indian_spot-billed_duckrotation": 7,
        "asian_wooly-necked_storkrotation": 8,
        "bulbulrotation": 9,
        "barn_owlrotation": 10,
        "woodpeakerrotation": 11,
        "yellow_breasted_greenfinchrotation": 12,
        "red_bearded_bea_eaterrotation": 13,
        "wrenrotation": 14,
        "black_kiterotation": 15,
        "brahminy_kiterotation": 16
    }
    return class_mapping.get(row_label, None)

def create_tf_example(group, path):
    file_name = str(group.filename.iloc[0]) + ".jpg"  # Ensure file_name is a string
    file_path = os.path.join(path, file_name)

    with tf.io.gfile.GFile(file_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = file_name.encode('utf8')
    image_format = b'jpg'
    xmins = [group.xmin / width]
    xmaxs = [group.xmax / width]
    ymins = [group.ymin / height]
    ymaxs = [group.ymax / height]
    classes_text = group['class'].encode('utf8')
    classes = class_text_to_int(group['class'])

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_feature(classes_text),
        'image/object/class/label': dataset_util.int64_feature(classes),
    }))
    return tf_example

def main(csv_file, output_tfrecord, image_folder):
    examples = pd.read_csv(csv_file)
    writer = tf.io.TFRecordWriter(output_tfrecord)
    for index, group in examples.groupby('filename'):
        tf_example = create_tf_example(group, image_folder)
        if tf_example:
            writer.write(tf_example.SerializeToString())
    writer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', required=True, help='Input CSV file path')
    parser.add_argument('--output_tfrecord', required=True, help='Output TFRecord file path')
    parser.add_argument('--image_folder', required=True, help='Path to image folder')
    args = parser.parse_args()
    main(args.csv_file, args.output_tfrecord, args.image_folder)
