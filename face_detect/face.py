import cv2
# 几乎一致的结果
#model_bin = "D:/Project_Anonymization/Anonymization-of-Dashcam-Recordings/face_detect/dnn_model/Tensorflow/opencv_face_detector_uint8.pb"
#config_text = "D:/Project_Anonymization/Anonymization-of-Dashcam-Recordings/face_detect/dnn_model/Tensorflow/opencv_face_detector.pbtxt"

model_bin = "D:/Project_Anonymization/Anonymization-of-Dashcam-Recordings/face_detect/dnn_model/Caffe/res10_300x300_ssd_iter_140000_fp16.caffemodel"
config_text = "D:/Project_Anonymization/Anonymization-of-Dashcam-Recordings/face_detect/dnn_model/Caffe/deploy.prototxt"

# load tensorflow model
net = cv2.dnn.readNetFromCaffe(config_text,model_bin)

#net = cv2.dnn.readNetFromTensorflow(model_bin, config=config_text)

#image = cv2.imread("D:\Project_Anonymization\Anonymization-of-Dashcam-Recordings/res\output_merged_boxes\img31_2.jpg")
image = cv2.imread("C:/Users/lirui/Desktop/image.jpg")
h = image.shape[0]
w = image.shape[1]

# 人脸检测
blobImage = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
net.setInput(blobImage)
Out = net.forward()

t, _ = net.getPerfProfile()
#label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
#cv2.putText(image, label, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# 绘制检测矩形
for detection in Out[0,0,:,:]:
    score = float(detection[2])
    objIndex = int(detection[1])
    if score > 0.4:
        left = detection[3]*w
        top = detection[4]*h
        right = detection[5]*w
        bottom = detection[6]*h

        # 绘制
        cv2.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0), thickness=2)
        print(score)
        cv2.putText(image, "score:%.2f"%score, (int(left), int(top)-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

cv2.imshow('demo', image)
cv2.waitKey(0)