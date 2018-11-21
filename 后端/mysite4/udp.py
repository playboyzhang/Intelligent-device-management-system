#!/usr/bin/env python
# -*- coding:UTF-8 -*-



#socket服务端
import socket
from time import ctime
import MySQLdb as mdb
import json
#设定地址端口
HOST = '172.19.193.222'
PORT = 20000
BUFSIZE = 4096

ADDR = (HOST,PORT)
#绑定套接字
udpSerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSerSock.bind(ADDR)

#连接数据库
try:
    conn = mdb.connect(
        host='47.94.211.235',
        port=3306,
        user='root',
        passwd='bishe@db',
        db='projectdb',
        charset='utf8',
        compress=1,
        connect_timeout=1
    )
except BaseException:
    print "Could not connect to MySQL server."
    exit(1)
#获取数据库游标
cus=conn.cursor()
#等待发送数据
while True:
    print 'wating for message...'
    data, addr = udpSerSock.recvfrom(BUFSIZE)
    #接收数据
    #udpSerSock.sendto('[%s] %s' % (ctime(), data), addr)
    print 'received from ',addr,'data:',data
    result=json.loads(data)
    #对接收的数据json化
    print(result)
    #对接收到的字符进行解析
    for row in result:
        #执行更新订单表
        flag=row["flag"]
        print(flag)
        if flag == '1':
            # 执行插入statistics表
            id = row["tab.ID"]
            print(id)
            type = row["tab.DEVICE_TYPE"]
            print(type)
            device_type = row["tab.DEVICE_ID"]
            print(device_type)
            val = row["tab.val"]
            print(val)
            mold = row["tab.MOLD"]
            print(mold)
            desc = row["tab.description"]
            print(desc)
            tim = row["tab.STIME"]
            print(tim)
            # 插入到数据库中
            sql = "insert into statistics (id,device_type,device_id,val,mold,description,stime) VALUES( " + '\'' + id + '\'' + ',' + '\'' + type + '\'' + ',' + '\'' + device_type + '\'' + ',' + '\'' + val + '\'' + ',' + '\'' + mold + '\'' + ',' + '\'' + desc + '\'' + ',' + '\'' + tim + '\'' + ")"
            # sql="insert into statistics (id,device_type,device_id,val,mold,description,stime) VALUES('%s,%s,%s,%s,%s,%s,%s,%s')" %(id,type,device_type,val,mold,desc,tim)
            cus.execute(sql)
            conn.commit()
            print("insert done")
        elif flag == '2':
            oid = row["id"]
            print(oid)
            sta = row["sta"]
            print(sta)
            tim = row["tim"]
            #start = row["start"]
            #print(start)
            #finish = row["finish"]
            #print(finish)
            if sta == "Done":
                sal="update order_detail set status="+'\''+sta+'\'' +',finishtime='+'\''+tim+'\''+' where id='+'\''+oid+'\''
                cus.execute(sal)
                conn.commit()
            elif sta == "Executing":
                sl="update order_detail set status="+'\''+sta+'\'' +',starttime='+'\''+tim+'\''+' where id='+'\''+oid+'\''
                cus.execute(sl)
                conn.commit()
            print("update done")
        else:
            print("error")
udpSerSock.close()