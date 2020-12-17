import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt
Blue = 138
Green = 63
Red = 23
THRESHOLD = 50
ANGLE = -45
MIN_AREA = 2000
LICENSE_WIDTH = 440
LICENSE_HIGH = 140

#绘图展示(后期放入工具类中)
def cv_show(name,img):
    cv2.namedWindow(name,0)
    print(img.shape)
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

MAX_WIDTH = 640
# 设置参数
#parser = argparse.ArgumentParser()
#parser.add_argument("-i", "image", required=True,help="D:/Project_Anonymization/Anonymization-of-Dashcam-Recordings/res/Anon_picked_randomName/1a0f355e-680f-4220-8727-87d91b5cf6b7.jpg") #image是变量名
#args = vars(parser.parse_args())

#读取原图像
img = cv2.imread("C:/Users/lirui/Desktop/incar.jpg")
cv_show('img',img)
img_hight, img_width = img.shape[:2]

#-------------------------------预处理--------------------------------------
#对图像进行缩放处理
if img_width > MAX_WIDTH:
    resize_rate = MAX_WIDTH / img_width
    img = cv2.resize(img,(MAX_WIDTH,int(img_hight * resize_rate)),interpolation=cv2.INTER_AREA)
# cv_show('img_resize',img)

# 高斯平滑
img_aussian = cv2.GaussianBlur(img,(5,5),1)
# cv_show('img_aussian',img_aussian)

#中值滤波
img_median = cv2.medianBlur(img_aussian,3)
# cv_show('img_median',img_median)
# print('width：',img_median.shape[:2][0])
# print('h',img_median.shape[:2][1])
#------------------------------车牌定位-------------------------------------
#分离通道
img_B = cv2.split(img_median)[0]
img_G = cv2.split(img_median)[1]
img_R = cv2.split(img_median)[2]
# print(img_B)
# print(img_G)
# print(img_R)
for i in range(img_median.shape[:2][0]):
    for j in range(img_median.shape[:2][1]):
        if abs(img_B[i,j] - Blue) < THRESHOLD and abs(img_G[i,j] - Green) <THRESHOLD and abs(img_R[i,j] - Red) < THRESHOLD:
            img_median[i][j][0] = 255
            img_median[i][j][1] = 255
            img_median[i][j][2] = 255
        else:
            img_median[i][j][0] = 0
            img_median[i][j][1] = 0
            img_median[i][j][2] = 0
cv_show('img_median',img_median)

kernel = np.ones((3,3),np.uint8)
img_dilate = cv2.dilate(img_median,kernel,iterations = 5) #膨胀操作
img_erosion = cv2.erode(img_dilate,kernel,iterations = 5) #腐蚀操作
cv_show('img_erosion',img_erosion)
img1 = cv2.cvtColor(img_erosion,cv2.COLOR_RGB2GRAY)
# cv_show('img1',img1)
image, contours, hierarchy = cv2.findContours(img1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# for i in range(len(contours)):
#     print(contours[i])

car_contours = []
for cnt in contours: #TODO：此处需要一个异常处理（因为有可能/0）
    # 框选 生成最小外接矩形 返回值（中心(x,y), (宽,高), 旋转角度）rect[0]：矩形中心点坐标；rect[1]：矩形的高和宽；rect[2]：矩形的旋转角度
    rect = cv2.minAreaRect(cnt)
    # print('宽高:',rect[1])
    area_width, area_height = rect[1]
    #计算最小矩形的面积，初步筛选
    area = rect[1][0] * rect[1][1] #最小矩形的面积
    if area > MIN_AREA:
        # 选择宽大于高的区域
        if area_width < area_height:
            area_width, area_height = area_height, area_width
        wh_ratio = area_width / area_height
        # print('宽高比：',wh_ratio)
        # 要求矩形区域长宽比在2到5.5之间，2到5.5是车牌的长宽比，其余的矩形排除
        if wh_ratio > 2 and wh_ratio < 5.5:
            car_contours.append(rect)  # rect是minAreaRect的返回值，根据minAreaRect的返回值计算矩形的四个点
            box = cv2.boxPoints(rect)  # box里面放的是最小矩形的四个顶点坐标
            box = np.int0(box)  # 取整
            # for i in range(len(box)):
            #     print('最小矩形的四个点坐标：', box[i])
            # 获取四个顶点坐标
            left_point_x = np.min(box[:, 0])
            right_point_x = np.max(box[:, 0])
            top_point_y = np.min(box[:, 1])
            bottom_point_y = np.max(box[:, 1])
            left_point_y = box[:, 1][np.where(box[:, 0] == left_point_x)][0]
            right_point_y = box[:, 1][np.where(box[:, 0] == right_point_x)][0]
            top_point_x = box[:, 0][np.where(box[:, 1] == top_point_y)][0]
            bottom_point_x = box[:, 0][np.where(box[:, 1] == bottom_point_y)][0]
            vertices = np.array([[top_point_x, top_point_y], [bottom_point_x, bottom_point_y], [left_point_x, left_point_y],[right_point_x, right_point_y]])
        oldimg = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        # print(car_contours)
        cv_show('oldimg', oldimg)