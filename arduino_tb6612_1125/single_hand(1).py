
import mediapipe as mp
import cv2
import numpy as np
import time
import socket

server_ip = '172.20.10.2'  # 树莓派的ip地址，根据连接的WIFI不同变化，学习的MGuest用不了，有防火墙
# server_ip = '35.0.31.255'
server_port = 12345 # 与服务器脚本相同的端口

def send_result2pi(str_guester):
    print(str_guester)
    command = str(str_guester)
    client_socket.send(command.encode())
    return True

def get_angle(v1, v2):

    angle = np.dot(v1, v2) / (np.sqrt(np.sum(v1 * v1)) * np.sqrt(np.sum(v2 * v2)))
    angle = np.arccos(angle) / 3.14 * 180

    return angle

def get_str_guester(up_fingers, list_lms, handness, hand_landmarks, mp_hands):
    if handness == 'Right hand':
        if len(up_fingers) == 1 and up_fingers[0] == 8:

            str_guester = "Go!"
            gesture_n = 1

        elif len(up_fingers) == 1 and up_fingers[0] == 4:
            # 获取大拇指的关键点坐标
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # 获取食指的关键点坐标
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # 判断大拇指和食指的垂直位置关系
            if thumb_tip.y > index_tip.y:
                str_guester = "Arm down"
                gesture_n = 9
            else:
                str_guester = "Arm up"
                gesture_n = 10

        elif len(up_fingers) == 2 and up_fingers[0] == 8 and up_fingers[1] == 12:
            str_guester = "Forward left!"
            gesture_n = 3

        elif len(up_fingers) == 3 and up_fingers[0] == 8 and up_fingers[1] == 12 and up_fingers[2] == 16:
            str_guester = "Forward right!"
            gesture_n = 4

        elif len(up_fingers) == 5:
            str_guester = "hand open!"
            gesture_n = 8

        elif len(up_fingers) == 0:
            str_guester = "hand close"
            gesture_n = 7

        elif len(up_fingers) == 2 and up_fingers[0] == 4 and up_fingers[1] == 8:
            str_guester = "Distance"
            gesture_n = 13
        else:
            str_guester = "None"
            gesture_n = 0

    else:  # left hand
        if len(up_fingers) == 1 and up_fingers[0] == 8:

            str_guester = "Back!"
            gesture_n = 2

        elif len(up_fingers) == 1 and up_fingers[0] == 4:
            str_guester = "Fast mode"
            gesture_n = 14

        elif len(up_fingers) == 1 and up_fingers[0] == 20:
            str_guester = "slow mode"
            gesture_n = 12

        elif len(up_fingers) == 2 and up_fingers[0] == 4 and up_fingers[1] == 8:
            str_guester = "Distance"
            gesture_n = 13

        elif len(up_fingers) == 2 and up_fingers[0] == 8 and up_fingers[1] == 12:
            str_guester = "Backward left!"
            gesture_n = 5

        elif len(up_fingers) == 3 and up_fingers[0] == 8 and up_fingers[1] == 12 and up_fingers[2] == 16:
            str_guester = "Backward right!"
            gesture_n = 6

        else:
            str_guester = "None"
            gesture_n = 0

    return str_guester,gesture_n

def command_buffer(N):
    buffer = [0] * N

    while True:
        print('buffer:',buffer)
        input_value = yield max(buffer, key=buffer.count)
        print('input_value:',input_value)
        buffer.pop(0)
        buffer.append(input_value if input_value is not None else 0)
def show_result(n):

    if n == 0:
        str_guester = "None"
    elif n ==1:
        str_guester = "Go!"
    elif n == 2:
        str_guester = "Back!"
    elif n ==3:
        str_guester = "Forward left!"
    elif n == 4:
        str_guester = "Forward right!"
    elif n == 5:
        str_guester = "Backward left!"
    elif n == 6:
        str_guester = "Backward right!"
    elif n == 7:
        str_guester = "hand close"
    elif n == 8:
        str_guester = "hand open!"
    elif n == 9:
        str_guester = "Arm down"
    elif n == 10:
        str_guester = "Arm up"
    elif n == 14:
        str_guester = "Fast mode"
    elif n == 12:
        str_guester = "slow mode"
    elif n == 13:
        str_guester = "Distance"

    return str_guester





if __name__ == "__main__":

    # 主动初始化TCP服务器连接
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # 定义手 检测对象
    mpHands = mp.solutions.hands
    hands = mpHands.Hands() # 默认是视频模式，可跟踪
    mpDraw = mp.solutions.drawing_utils
    # 设置 列表存储 控制时间
    gesture_list = []
    none_list = []

    N = 10  # length of buffer
    com_buffer = command_buffer(N)
    com_buffer.send(None)
    cv2.namedWindow('hands', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('hands',800,600)

    while True:
        str_gesture = "None"
        start_time = time.time()
        # 读取一帧图像
        success, img = cap.read()
        if not success:
            continue
        image_height, image_width, _ = np.shape(img)

        # 转换为RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 得到检测结果
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0] #只取一只手
            handedness = results.multi_handedness[0]
            if handedness.classification[0].label == 'Left':
                # print("右手")
                str_handedness = 'Right hand'
            else:
                # print("左手")
                str_handedness = 'Left hand'
            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)

            # 采集所有关键点的坐标
            list_lms = []
            for i in range(21):
                pos_x = hand.landmark[i].x * image_width
                pos_y = hand.landmark[i].y * image_height
                list_lms.append([int(pos_x), int(pos_y)])

            # 构造凸包点
            list_lms = np.array(list_lms, dtype=np.int32)
            hull_index = [0, 1, 2, 3, 6, 10, 14, 19, 18, 17, 10]
            hull = cv2.convexHull(list_lms[hull_index, :])
            # 绘制凸包
            cv2.polylines(img, [hull], True, (0, 255, 0), 2)

            # 查找外部的点数
            n_fig = -1
            ll = [4, 8, 12, 16, 20]
            up_fingers = []

            for i in ll:
                pt = (int(list_lms[i][0]), int(list_lms[i][1]))
                dist = cv2.pointPolygonTest(hull, pt, True)
                if dist < 0:
                    up_fingers.append(i)

            str_gesture, gesture_n = get_str_guester(up_fingers, list_lms, str_handedness, hand, mpHands)
            # cv2.putText(img, str_handedness + ':' + ' %s' % (str_gesture), (90, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4,
            #             cv2.LINE_AA)

            for i in ll:
                pos_x = hand.landmark[i].x * image_width
                pos_y = hand.landmark[i].y * image_height
                # 画点
                cv2.circle(img, (int(pos_x), int(pos_y)), 3, (0, 255, 255), -1)

            final_result = com_buffer.send(gesture_n)
            str_gesture = show_result(final_result)
            cv2.putText(img, str_handedness + ':' + ' %s' % (str_gesture), (90, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4,
                        cv2.LINE_AA)
            gesture_list.append(gesture_n)

            if len(gesture_list) == 3:
                result = final_result
                send_result2pi(result)
                time.sleep(0.1)
                gesture_list = []
        else:
            final_result = com_buffer.send(0)
            gesture_list.append(0)
            if len(gesture_list) == 3:
                result = final_result
                send_result2pi(result)
                time.sleep(0.1)
                gesture_list = []
        cv2.imshow("hands", img)

        end_time = time.time()
        process_time = end_time - start_time
        print(f'Process time for one frame:{process_time}, {1/process_time} frames per second')
        print(str_gesture)

        # 按下Esc键退出循环
        if cv2.waitKey(1) == 27:
            break

    client_socket.close()
    cap.release()
    cv2.destroyAllWindows()













