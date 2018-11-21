#!/usr/bin/env python
# -*- coding: utf-8 -*-

#UDP客户端

import socket,time


def sendMessage(msm):
    HOST = '172.19.193.222'
    PORT =  10000
   #BUFSIZE = 1024
    ADDR = (HOST, PORT)
    udpCliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpCliSock.connect(ADDR)
    time.sleep(0.5)
    data = msm
    try:
        udpCliSock.sendto(data.encode('utf-8'), ADDR)  # 发送数据
        #data, ADDR = udpCliSock.recvfrom(BUFSIZE)  # 接受数据
        #print 'Server : ', data
    except Exception, e:
        print 'Error: ', e
    udpCliSock.close()

    
  


