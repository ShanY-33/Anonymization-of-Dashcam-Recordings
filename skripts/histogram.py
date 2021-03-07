'''
create histogram of aspect ratio distribution
'''

import os
import numpy
import cv2
import matplotlib.pyplot as plt

f=open('..annots_file_path', 'r').readlines()

N = len(f)
i = 0
count = 0
data = []
while i < N:

    row=f[i].rstrip().split()
    #examples = pd.read_csv(FLAGS.csv_input)
    file_nam = row[0]
    if row[1] == '1':
        if os.path.exists('..annots_file_path/'+file_nam):
            img = cv2.imread('..annots_file_path/'+file_nam)
            height = img.shape[0]
            width = img.shape[1]
            if (float(row[3])-float(row[2]))*width >= 25.0:
                if (float(row[5])-float(row[4]))*height >= 30.0:
                    count += 1
                    aspect_ratio = (float(row[3])-float(row[2]))*width/(((float(row[5])-float(row[4]))*height)+0.001)
                    data.append(aspect_ratio)
    i += 1
    if count >= 7200:
        break
    

print(count)
plt.hist(data, bins=[ 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8])
plt.xlabel('Aspect Ratio')
plt.ylabel('Number of Object')
plt.show()

