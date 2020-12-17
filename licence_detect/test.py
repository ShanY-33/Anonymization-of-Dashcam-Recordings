from cv2 import cv2
import numpy as np
import os

lower_blue = np.array([90,90,0])
upper_blue = np.array([120,210,250])


img = cv2.imread('C:/Users/lirui/Desktop/car4.jpeg')
# 设置图片的比例，只有图片的显示面积合适，才能定位出车牌，需要调节
n = 1.5
sp = img.shape
height = round(n*sp[0])
weight = round(n*sp[1])
new_img = cv2.resize(img,(weight,height))
#cv2.imshow('img', new_img)

hsv = cv2.cvtColor(new_img, cv2.COLOR_BGR2HSV)
mark = cv2.inRange(hsv, lower_blue, upper_blue)
# 形态学分割是识别的白色区域。如果在mark中车牌的颜色是黑色，需要翻转
# mark = cv2.bitwise_not(mark)
#cv2.imshow("mark", mark)

# 腐蚀和膨胀
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,5))         #定义矩形结构元素
# 腐蚀和膨胀的次数也可以根据情况调节
img_erode = cv2.erode(mark, kernel, iterations=1)
img_dilated = cv2.dilate(mark, kernel, iterations=3)
#cv2.imshow('erode', img_dilated)

# 寻找轮廓
contours, hierarchy = cv2.findContours(img_dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if area > 4000:
        
        rect = cv2.minAreaRect(contours[i]) #提取矩形坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)  
        angle =abs(abs(rect[2])-45) 
        length = max(rect[1])
        wideth = min(rect[1])
        bili = length / (wideth + 0.01)
        
        area = rect[1][0] * rect[1][1]
         
        if  area > 20000 or angle < 30:
            continue
        
        
        if bili > 3.3 or bili < 2.5 :
            continue
        print(area)        
        print(bili)  
        print(rect[2])  

        cv2.drawContours(new_img, [box], 0, (0, 0, 255), 2) 
        
        

cv2.imshow('result', new_img)
cv2.waitKey(0)