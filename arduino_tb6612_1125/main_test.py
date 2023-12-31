import socket
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
import argparse
import serial
import sys
import time

arduino_port = '/dev/ttyUSB0'  # Arduino Serial port

# initialize Serial port for Teensy connection
ser = serial.Serial()
ser.port = arduino_port  # Teensy Serial port
ser.baudrate = 115200
ser.timeout = None  # specify timeout when using readline()
#ser.reset_input_buffer()
time.sleep(3)
print("Serial OK")
ser.open()
time.sleep(0.1)

KNOWN_DISTANCE = 15  # 初始化D，为了计算相机焦距
KNOWN_WIDTH = 5.08 # W， 物体的实际宽度

# Flag for indicating how we perform ball localization
USE_LOCALIZATION_HEURISTIC = True
# Flag to indicate computation method for localization heuristic
USE_IDX_IMG = True

# Values for color thresholding (default trackbar values)
H_val = 70  # H-value of ball for difference image
thold_val = 3  # Threshold value for difference image


camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
def trackchan_hue(x):
    global H_val
    H_val = x


def trackchan_tg(x):
    global thold_val
    thold_val = x


hh = 'hue'
hl = 'threshold'

title_window = 'trackbar'
cv2.namedWindow(title_window)

cv2.createTrackbar("hue", title_window, H_val, 255 ,trackchan_hue)
cv2.createTrackbar("thresh", title_window, thold_val, 50, trackchan_tg)

def send_result2mcu(result):
    # serial
    ser.write((result + "\n").encode()) #need to fix
    line = ser.readline().decode().rstrip()
    print(line)
    time.sleep(0.1)
    return

def color_subtract(img, color):
    # print(img.shape)
    # TODO: Convert img to HSV format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # print(img.shape)
    # # TODO: Extract only h-values (2D Array)
    img = img[:, :, 0]
    # # TODO: Take the difference of each pixel and the chosen H-value
    # # HINT: Pay attention to integer overflow here. What happens when
    # # subtracting unsigned ints and the result is negative?
    # # Use integer casting before you subtract and take the absolute value, then
    # # use it again when you return a 2D array of unsigned ints as your difference image

    diff = np.abs((img.astype('int16') - color))

    # TODO: Take absolute value of the pixels
    # cv2.imshow("diff",diff)
    diff = diff.astype('uint8')
    final_img = diff

    return final_img

# Function to find the centroid and radius of a detected region
# Inputs:
#   img         Binary image
#   USE_IDX_IMG Binary flag. If true, use the index image in calculations; if
#               false, use a double nested for loop.
# Outputs:
#   center      2-tuple denoting centroid
#   radius      Radius of found circle
def identify_ball(img, USE_IDX_IMG):
    # Find centroid and number of pixels considered valid
    h, w = img.shape

    # Double-nested for loop code
    if USE_IDX_IMG == False:
        k = 0
        x_sum = 0
        y_sum = 0
        for y in range(w):
            for x in range(h):
                if img[x, y] != 0:
                    k += 1  # Uncomment this line when editing here+
                    x_sum += x
                    y_sum += y
                    # TODO: Calculate x_sum, y_sum, and k

        if (k != 0):
            # TODO: Calculate the center and radius using x_sum, y_sum, and k.
            c_x = int(x_sum / k)
            c_y = int(y_sum / k)
            r = np.sqrt(k / np.pi)

        else:
            # TODO: Don't forget to account for the boundary condition where k = 0.
            c_x = 0
            c_y = 0
            r = 0
        center = (c_x, c_y)
        radius = int(r)

    # Use index image
    else:
        # Calculate number of orange pixels
        k = np.sum(img)
        # print(k)

        if k == 0:
            # No orange pixels.  Return some default value
            return (0, 0), 0

        # Index image vectors
        # x_idx = np.expand_dims(np.arange(w),0)
        # y_idx = np.expand_dims(np.arange(h),1)
        # print(x_idx)  #(1,640)
        # print(y_idx.shape)  #(480,1)

        # x_idx = np.arange(w)
        # x_idx = np.tile(x_idx, (h, 1))
        # y_idx = np.arange(h).reshape(-1, 1)
        # y_idx = np.tile(y_idx, (1, w))
      
        # masked_index_image = x_idx * img
        # weighted_sum_x = np.sum(masked_index_image, axis=1)
        # c_x = int(np.sum(weighted_sum_x) / k)
        # print(np.sum(weighted_sum_x))
        # c_x = np.abs(c_x)

        # masked_index_image = y_idx * img
        # weighted_sum_y = np.sum(masked_index_image, axis=0)
        # c_y = int(np.sum(weighted_sum_y) / k)
        # c_y = np.abs(c_y)

        # center = (c_x, c_y)
        # radius = int(np.sqrt(k / 255)/2)

 # Index image vectors
        x_idx = np.expand_dims(np.arange(w),0)
        y_idx = np.expand_dims(np.arange(h),1)
        # print(x_idx.shape, y_idx.shape)
        # print(k, img.shape)

        # TODO: Calculate the center and radius using the index image vectors
        #       and numpy commands
        C_x = (x_idx @ img.T) / k
        C_y = (img.T @ y_idx) / k
        # print(C_x.shape, C_y.shape)
        C_x = int(np.sum(C_x))
        C_y = int(np.sum(C_y))

        # print(C_x, C_y)
        center = (C_x, C_y)
        radius = int(np.sqrt(k / 255)/2)
        # print(radius)

    # print(center)
    # print(radius)
    return center, radius

def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

def draw_item(x,y,r,image):
    x1 = x-r
    y1 = y-r
    x2 = x+r
    y2 = y-r
    x3 = x+r
    y3 = y+r
    x4 = x-r
    y4 = y+r

    square_points = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]],np.int32)

    square_points = square_points.reshape((-1,1,2))
    # print(square_points)
    cv2.polylines(image,[square_points],isClosed = True,color = (0, 255, 0),thickness = 3)
    
def focallength(image):
    flag = 0
    diff = color_subtract(image, H_val)
    diff = cv2.boxFilter(diff, -1, (5, 5))
    _, thresh = cv2.threshold(diff, thold_val, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('thresh',thresh)
    center, radius = identify_ball(thresh, USE_IDX_IMG)
    print(center)
    print(radius)
    # center = (320,240)
    # radius = 50
 
    # cv2.circle(image, center, radius, (0, 255, 0), 2)
    draw_item(center[0],center[1],radius,image)
    focal_l = 435
    try:
        distance = distance_to_camera(KNOWN_WIDTH, focal_l, 2*radius)
           
        if 280<=center[0]<=360:
            flag = 1
        dis = "{:.2f}".format(distance)
        print('distance:',dis)
        cv2.putText(image, dis+'cm', (370, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4,
                    cv2.LINE_AA)
        if 9.5<=distance <=12.8:
            if flag == 1:
                cv2.putText(image,'In range,In the middle!', (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 4,
                cv2.LINE_AA)
            else:
                cv2.putText(image,'In range,Not in the middle', (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4,
                cv2.LINE_AA)
        else:
            cv2.putText(image,'Not in range', (160, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4,
                cv2.LINE_AA)
    except ZeroDivisionError:
        cv2.putText(image, 'Too far', (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4,
            cv2.LINE_AA)

    return True


# 服务器配置
host = '0.0.0.0'  # 监听所有可用的网络接口
port = 12345  # 选择一个未被占用的端口

# 创建服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)  # 只接受一个客户端连接

print(f"Monitoring from {host}:{port}...")

client_socket, client_address = server_socket.accept()
print(f"Successful request from {client_address}")
mode_text = 'Fast'
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    s = time.time()

    image = frame.array
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # plt.figure()
    # plt.imshow(image)
    # plt.show()
    # print('#'*20)
    command = client_socket.recv(1024).decode()
    print(command)
    send_result2mcu(command)
    # command = "13"
    if not command:
        break
    if command == "14":
        mode_text = 'Fast'
    if command == '12':
        mode_text = 'Slow'
    if command == "13":
        # activate auto pick up
        focallength(image)
    cv2.putText(image, mode_text, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 0, 0), 4,
                    cv2.LINE_AA)
    cv2.imshow("Real-time Image", image) #comment out when debugging
    # Get keypress
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if key == ord("q"):
    #     break

    e = time.time()
    print(f'pi receive from pc:{command},process_time:{e-s}')

cv2.destroyAllWindows()
client_socket.close()
server_socket.close()

ser.close()
