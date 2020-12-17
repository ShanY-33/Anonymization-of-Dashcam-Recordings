import cv2
import mtcnn
#from mtcnn import MTCNN

detector = mtcnn.MTCNN(min_face_size=5)
img = cv2.imread("C:/Users/lirui/Desktop/img1_1.jpg")
detected = detector.detect_faces(img)

if len(detected) > 0:  # 大于0则检测到人脸
    print("the number of face is :",len(detected))
    for i, d in enumerate(detected):  # 单独框出每一张人脸
        x1, y1, w, h = d['box']
        x2 = x1 + w
        y2 = y1 + h
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), thickness=2)

cv2.imshow('demo', img)
cv2.waitKey(0)