'''
generate tfrecord according to Tensorflow generate_tfrecord.py
'''
# -*- coding: utf-8 -*-
 
"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python oid_tfrecord.py --txt_input=train/annots_merge.txt  --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
import os
import time
import io
import pandas as pd
import tensorflow as tf
 
from PIL import Image
from object_detection.utils import dataset_util
 
flags = tf.app.flags
flags.DEFINE_string('txt_input', '', 'Path to the TXT input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

def class_int_to_text(row_label):
    if row_label == '1':
        return 'Human face'
    elif row_label == '2':
        return 'Vehicle registration plate'
    else:
        None
 
def create_tf_example(f, line_num):
    #full_path = os.path.join(os.getcwd(), 'images', '{}'.format(row['filename']))
    xmins = []  # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = []  # List of normalized right x coordinates in bounding box (1 per box)
    ymins = []  # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = []  # List of normalized bottom y coordinates in bounding box (1 per box)
    classes_text = []  # List of string class name of bounding box (1 per box)
    classes = []  # List of integer class id of bounding box (1 per box)
    occluded = []
    valid_img = 0
    valid_plate = 0

    first_row = f[line_num].rstrip().split()
    old_name = first_row[0]
    full_path = os.path.join(os.path.dirname(FLAGS.txt_input), 'images', '{}'.format(old_name))
    with tf.gfile.GFile(full_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size
    filename = old_name.encode('utf8')
    image_format = b'jpg'

    while old_name == f[line_num].rstrip().split()[0]:
        row = f[line_num].rstrip().split()
        '''
        full_path = os.path.join(os.path.dirname(FLAGS.txt_input), 'images', '{}'.format(row[0]))
        with tf.gfile.GFile(full_path, 'rb') as fid:
            encoded_jpg = fid.read()
        encoded_jpg_io = io.BytesIO(encoded_jpg)
        image = Image.open(encoded_jpg_io)
        width, height = image.size
        filename = row[0].encode('utf8')
        image_format = b'jpg'
        '''
        #confidence = [float(row[1])]
        if row[0].split('/')[0] == 'open_images':
            valid_plate += 1
            xmins.append(float(row[2]))
            xmaxs.append(float(row[3]))
            ymins.append(float(row[4]))
            ymaxs.append(float(row[5]))
            classes_text.append(class_int_to_text(row[1]).encode('utf8'))
            classes.append(int(row[1]))
            #truncated = [int(row[7])]
            occluded.append(int(row[6]))
            #group_of = [int(row[8])]
            #depiction = [int(row[9])]

        elif float(row[3])-float(row[2]) > 25.0:
            if float(row[5])-float(row[4]) > 30.0:
                valid_img += 1
                xmins.append(max(0.005, (float(row[2]) / width)))
                xmaxs.append(min(0.995, (float(row[3]) / width)))
                ymins.append(max(0.005, (float(row[4]) / height)))
                ymaxs.append(min(0.995, (float(row[5])/ height)))
                classes_text.append(class_int_to_text(row[1]).encode('utf8'))
                classes.append(int(row[1]))
                #truncated = [int(row[7])]
                occluded.append(int(row[6]))
                #group_of = [int(row[8])]
                #depiction = [int(row[9])]
    
        old_name = row[0]
        line_num += 1
        if line_num == len(f):
            break

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        #'image/class/confidence': dataset_util.float_list_feature(confidence),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
        #'image/object/truncated': dataset_util.int64_list_feature(truncated),
        'image/object/occluded': dataset_util.int64_list_feature(occluded),
        #'image/object/group_of': dataset_util.int64_list_feature(group_of),
        #'image/object/depiction': dataset_util.int64_list_feature(depiction),
    }))

    return line_num-1, tf_example, valid_img, valid_plate
 
def main(_):
    writer = tf.io.TFRecordWriter(FLAGS.output_path)
    f=open(FLAGS.txt_input, 'r').readlines()

    N = len(f)
    count = 0
    plate = 0
    i = 0

    while i < N:
        #print(i)
        row=f[i].rstrip().split()
        #examples = pd.read_csv(FLAGS.csv_input)
        file_nam = row[0]

        if os.path.exists('/home/ruili/models/research/object_detection/data/train/images/'+file_nam):

            line_num, tf_example, valid_img, valid_plate = create_tf_example(f,i)
            if valid_plate != 0:
                writer.write(tf_example.SerializeToString())
                plate += 1

            if valid_img != 0:    
                count += 1
                writer.write(tf_example.SerializeToString())
            
            i = line_num

        i += 1


    print("Valid wider_images number is %d" % count)
    print("Valid oid number is %d" % plate)

    writer.close()
 
if __name__ == '__main__':
    tf.compat.v1.app.run()
