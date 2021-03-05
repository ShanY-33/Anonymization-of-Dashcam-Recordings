'''
This sccript is used to download several specific classes from Open Image dataset
'''
import csv
import subprocess
import os
 
#choose dataset(train/test)
setName = "train"
#choose class
classes = ["Human face","Vehicle registration plate"]
 
#parse class-descriptions-boxable.csv file into a dictionary
with open('class-descriptions-boxable.csv', mode='r') as infile:
    reader = csv.reader(infile)
    dict_list = {rows[1]:rows[0] for rows in reader}
 
#create image folder
subprocess.run(['rm', '-rf', 'Images'])
subprocess.run([ 'mkdir', 'Images'])

#create label folder
subprocess.run(['rm', '-rf', 'Labels'])
subprocess.run([ 'mkdir', 'Labels'])

#find all annotations according to class code
commandStr = "grep -E" +' '+ dict_list[classes[0]]+'|'+dict_list[classes[1]] + " " + setName + "-annotations-bbox.csv"
class_annotations = subprocess.run(commandStr.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
class_annotations = class_annotations.splitlines()  

totalNumOfAnnotations = len(class_annotations)
print("Total number of annotations : "+str(totalNumOfAnnotations))
name_old = " "
count = 0
for line in class_annotations[0:totalNumOfAnnotations]:
    count = count + 1
    print("annotation count : " + str(count))

    lineParts = line.split(',')
    name_new = lineParts[0]
    #download
    if lineParts[0] != name_old:
        name_old = lineParts[0]
        subprocess.run([ 'aws', 's3', '--no-sign-request', '--only-show-errors', 'cp', 's3://open-images-dataset/'+setName+'/'+lineParts[0]+".jpg", 'Images/'+lineParts[0]+".jpg"])
    
    #choose several annotation part in a txt file
    label = int(2) if lineParts[2] == '/m/01jfm_' else int(1)
    with open('Labels/%s.txt'%('annots'),'a') as f:
        f.write(' '.join(['open_images/'+lineParts[0]+'.jpg', str(label), str(lineParts[4]), str(lineParts[5]), str(lineParts[6]), str(lineParts[7]), str(lineParts[8])])+'\n')


print('ready to next')
