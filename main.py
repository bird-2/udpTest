# 计算机网络小学期大作业 第四题
# 客户端接收视频，服务器端发送视频，客户端一运行就会链接服务端，首先会发送一个开始消息，然后开始接收来自服务端的视频消息

# -*- coding: utf-8 -*-
import socket
import cv2
import time
import numpy as np


def roleobject(role):
    # UDP发送
    # 服务端
    if role == "-s":
        # 实例化一个socket对象，套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind（）绑定IP和端口
        # python可以使用固定或不固定的端口发送UDP，若使用固定端口，需要绑定IP和端口号
        udp_socket.bind(('127.0.0.1', 9999))
        # 获得视频信息，打开视频
        cap = cv2.VideoCapture('send.mp4')
        # 视频文件中的帧数
        fram_all = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # 设置capture对象的属性，propid对应属性，value对应属性的值
        cap.set(4, 1920)
        cap.set(3, 1200)
        # 可以调整窗口大小，创建我们的窗口
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)

        for i in range(int(fram_all)):
            # udP接收数据和地址
            recvdata, addr = udp_socket.recvfrom(57600)
            if recvdata != '0':
                # cap.read()按帧读取视频，ret（_),frame(fra)是获cap.read()方法的两个返回值。
                # 其中ret是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。
                # fra就是每一帧的图像
                _, fra = cap.read()
                # 将图片格式转换(编码)成流数据，赋值到内存缓存中
                img_encode = cv2.imencode(".jpg", fra)[1]
                imde = cv2.imdecode(img_encode, 1)
                # 在窗口中显示，第一个参数是窗口名称，第二个是我们的图像
                cv2.imshow('img', imde)
                each_size = 30000
                msg_size = len(img_encode)
                print("msg size", msg_size)
                print("each size", each_size)
                # 将图片转换的数据流分成多少块
                loop_time = int(len(img_encode) / each_size)
                # 整除是商，不整除商加1
                extra = 1
                if len(img_encode) % each_size == 0:
                    extra = 0
                print("loop times", loop_time + extra)
                offset = 0
                # udp可以直接调用sendto函数，发送信息到指定的IP和端口号，addr为地址
                res = udp_socket.sendto(str(msg_size).encode("utf-8"), addr)
                total_send = 0
                # 确定要发送的数据，循环发送图像信息
                for j in range(loop_time):
                    data = img_encode[offset:offset + each_size][:]
                    offset += each_size
                    res = udp_socket.sendto(data, addr)
                    # 打印一下发送全部信息，把每次发送的数据量都记录下来
                    print(j, res)
                    total_send += res
                    time.sleep(0.01)
                # 判断一个是否还有最后一块，如果说余不为0，则需要发送末尾一块信息
                if extra == 1:
                    data = img_encode[offset:][:]
                    res = udp_socket.sendto(data, addr)
                    print(res)
                    total_send += res
                # 确定数据已经发送全部
                if total_send == msg_size:
                    print("complate")
                # cv2.waitKey()函数，参数是1，表示延时1ms切换到下一帧的图像；参数是0，表示只显示当前帧，即视频暂停
                cv2.waitKey(1)
        # 释放资源
        cap.release()
        udp_socket.close()
    # 客户端
    elif role == "-c":
        # 端口号和地址，这个是链接服务端的配置，地址可以随便设计，TCP端口号是724,只要不冲突就行
        port = 9999
        host = '127.0.0.1'
        # 实例化一个socket对象，一个套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 发送信息
        udp_socket.sendto(b'1', (host, port))
        # 调出窗体
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # 盛放接收数据的容器
        finish_data = bytes()
        # 总大小和当前大小
        total_size = 0
        current_size = 0
        while True:
            # 当前接收到的数据是一个新图片的开端
            if total_size == 0:
                # utf编码协议，编码出来的数据就是6长度
                data, addr = udp_socket.recvfrom(6)
                print(type(data))
                total_size = int(data.decode("utf-8"))
                print("total size", total_size)
            data, addr = udp_socket.recvfrom(30000)
            # 读到了这个数据，就进行操作一直接收数据
            if data:
                if current_size < total_size:
                    current_size += len(data)
                    print(len(data))
                    finish_data += data[:]
                    print(len(data))
                    if current_size == total_size:
                        print("Finish")
                        # frombuffer将data以流的形式读入转化成ndarray对象,第一个参数是缓冲区，表示在缓冲区接口的对象，dtype：代表返回的数据类型数组的数据类型。默认值为0。
                        recvData = np.frombuffer(finish_data, dtype=np.uint8)
                        imde = cv2.imdecode(recvData, 1)
                        # 在窗口中显示
                        cv2.imshow('img', imde)
                        # cv2.waitKey()函数，参数是1，表示延时1ms切换到下一帧的图像；参数是0，表示只显示当前帧，即视频暂停
                        k = cv2.waitKey(1)
                        # 判断当前视频是不是播放结束，如果播放完了就结束，没有就继续
                        finish_data = bytes()
                        current_size = 0
                        total_size = 0
                        # q是cv库中最后一帧的意思
                        if k == ord('q'):
                            print("ok")
                            udp_socket.sendto(b'0', port, host)
                        else:
                            udp_socket.sendto(b'1', port, host)
        # 释放资源
        udp_socket.close()
        # 关闭所有的窗口
        cv2.destroyAllWindows()
    else:
            print("unknown role", role)
            return
