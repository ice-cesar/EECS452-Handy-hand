import numpy as np
import cv2

# F 相机焦距 P物体的像素宽度

# step1  F = P * D / W
# step2  D' = F * W / P

KNOWN_DISTANCE = 30  # 初始化D，为了计算相机焦距
KNOWN_WIDTH = 27 # W， 物体的实际宽度

KNOWN_HEIGHT = 8.27


# 定义目标函数
def find_marker(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将彩色图转化为灰度图
    cv2.imshow("gray_img", gray_img)
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)  # 高斯平滑去噪
    cv2.imshow("gaussianblur_img", gray_img)
    edged_img = cv2.Canny(gray_img, 35, 125)  # Canny算子阈值化
    cv2.imshow("canny_img", edged_img)
    # 获取纸张的轮廓数据
    countours, hierarchy = cv2.findContours(edged_img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(countours))
    # 获取最大面积对应的点集
    c = max(countours, key=cv2.contourArea)
    # 最小外接矩形
    rect = cv2.minAreaRect(c)
    return rect


# 定义距离函数
def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth


# 计算摄像头的焦距（内参）
def calculate_focalDistance(img_path):
    first_image = cv2.imread(img_path)
    # cv2.imshow('first image', first_image)
    # 获取矩形的中心点坐标，长度，宽度和旋转角度
    marker = find_marker(first_image)
    print("origin图片中A4纸的宽度：", marker[1][0])
    focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
    print('焦距 = ', focalLength)
    return focalLength


# 计算摄像头到物体的距离
def calculate_Distance(image_path, focalLength_value):
    image = cv2.imread(image_path)
    # 获取矩形的中心点坐标，长度，宽度和旋转角度， marke[1][0]代表宽度
    marker = find_marker(image)
    distance_inches = distance_to_camera(KNOWN_WIDTH, focalLength_value, marker[1][0])
    box = cv2.boxPoints(marker)
    # print("Box = ", box)
    box = np.int0(box)
    # print("Box = ", box)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.putText(image, "%.2fcm" % (distance_inches * 2.54), (image.shape[1] - 1000, image.shape[0] - 100),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
    cv2.imshow("img", image)


if __name__ == "__main__":
    img_path = "phone30.jpg"
    focalLength = calculate_focalDistance(img_path)
    calculate_Distance("phone40.jpg", focalLength)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
