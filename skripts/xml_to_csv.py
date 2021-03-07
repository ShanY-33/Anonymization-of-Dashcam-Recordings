# xml_to_csv.py
# -*- coding: utf-8 -*-
 
import os, sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET
def xml_to_csv(_path, _out_file):
    xml_list = []
    for xml_file in glob.glob(_path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     round(float(member[4][0].text)),
                     round(float(member[4][1].text)),
                     round(float(member[4][2].text)),
                     round(float(member[4][3].text))
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    xml_df.to_csv(_out_file, index=None)
    print('Successfully converted xml to csv.')
 
if __name__ == '__main__':
    # convert
    xml_to_csv(sys.argv[1], sys.argv[2])