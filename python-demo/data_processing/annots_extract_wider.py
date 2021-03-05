import os
import subprocess

subprocess.run(['rm', '-rf', 'labels'])
subprocess.run([ 'mkdir', 'labels'])
 

annot = 'wider_face_train_bbx_gt.txt'
with open(annot) as f:
    name_old = ' '
    for filename in f:
        filename = filename.rstrip().split()
        if len(filename) == 1 and len(filename[0]) >= 5:
            name_old = filename[0]

        if len(filename) != 1:
            xmin = float(filename[0])
            ymin = float(filename[1])
            xmax = float(filename[0]) +float(filename[2])
            ymax = float(filename[1]) +float(filename[3])
            occlusion = int(0) if int(filename[8])==0 else int(1)
            with open('labels/%s.txt'%('wider_annots'),'a') as f:
                f.write(' '.join([name_old, str(1), str(xmin), str(xmax), str(ymin), str(ymax), str(occlusion)])+'\n')

    
#out = 'dataset/wider_face_train_no_resize.record'
#wider2tfrecord(annot, out)
