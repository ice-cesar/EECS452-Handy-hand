# import bluetooth
#
# server_address = "DC:A6:32:7E:7B:0F"  # 将这里替换为树莓派的蓝牙地址
# port = 0
# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# print(nearby_devices)#附近所有可连的蓝牙设备
# sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# sock.connect((server_address, port))
#
# try:
#     while True:
#         command = input("Enter a command for Raspberry Pi: ")
#         sock.send(command)
# except KeyboardInterrupt:
#     pass
#
# sock.close()

# import socket
# import bluetooth
# # 设置树莓派蓝牙地址和端口
# raspberry_pi_bluetooth_address = "DC:A6:32:7E:7B:0F"  # 请将 XX:XX:XX:XX:XX:XX 替换为树莓派的蓝牙地址
# port = 0
# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# print(nearby_devices)#附近所有可连的蓝牙设备
# client_socket = None  # 初始化 client_socket 变量
#
# try:
#     client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
#     client_socket.connect((raspberry_pi_bluetooth_address, port))
#
#     while True:
#         # 输入要发送的命令
#         command = input("Enter a command for Raspberry Pi (or 'exit' to quit): ")
#
#         if command == "exit":
#             break
#
#         # 发送命令到树莓派
#         client_socket.send(command.encode())
#
#         # 接收并打印树莓派的响应
#         response = client_socket.recv(1024).decode()
#         print("Response from Raspberry Pi:", response)
# # 其他代码
# except KeyboardInterrupt:
#     pass
# finally:
#     if client_socket:
#         client_socket.close()

# import socket
# import threading
#
# # 服务器配置
# server_ip = '10.0.0.251'  # pi ip address
# server_port = 12345
#
# # 创建客户端套接字
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((server_ip, server_port))
#
#
# # 客户端发送命令的函数
# def send_command():
#     while True:
#         command = input("PC输入命令 (led_on/led_off/exit): ")
#         client_socket.send(command.encode())
#
#         if command == "exit":
#             break
#
#
# # 客户端接收命令的函数
# def receive_command():
#     while True:
#         response = client_socket.recv(1024).decode()
#         print(f"树莓派的响应: {response}")
#
#
# # 启动发送和接收线程
# send_thread = threading.Thread(target=send_command)
# receive_thread = threading.Thread(target=receive_command)
#
# send_thread.start()
# receive_thread.start()
#
# send_thread.join()
# receive_thread.join()
#
# client_socket.close()


import socket

# 服务器配置
server_ip = '10.0.0.251'  # 根据实际情况替换
server_port = 12345  # 与服务器脚本相同的端口

# 创建客户端套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#主动初始化TCP服务器连接
client_socket.connect((server_ip, server_port))

while True:
    command = input("Type the command(led_on/led_off/exit): ")
    client_socket.send(command.encode())

    if command == "exit":
        break

client_socket.close()
