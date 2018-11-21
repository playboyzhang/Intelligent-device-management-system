# -*- coding: utf-8 -*-
 
from django.http import HttpRequest,HttpResponse  
from django.http import JsonResponse  
from json import dumps  
from django.core import serializers  
import json,string
from django.db import connection

from datetime import datetime
from . import  UDPClient





#获取创建订单的鹤位位置,并插入客户信息
def freeoilpipe(request):
    global cu_id
    global oil_val
    global t_date
    global date_str
    global cus_p
    global cus_c
    global cus_id



    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    #从前端接收到的油的种类
    oil_type=object[u'oil_type']
    #从前端接收到的油的体积
    oil_val=object[u'oil_val']
    #从前端接收到客户手机号
    cus_p=object[u'cus_phone']
    #从前端接收到客户车牌号
    cus_c=object[u'cus_cnumber']
    #从前端接收到身份证号
    cus_id=object[u'cus_idnumber']
    #订购日期??????
    t_date=object[u't_date'] 
    date=datetime.now()#登记产生的系统当前时间
    date_str=datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
    print(object)
    #查找出对应油的相关信息
    sql='select area.id,oilcan.id,oilpipe.id,oil.PRICE from area,oilcan,oilpipe,oil where oilcan.OIL_ID=oil.ID AND oilcan.AREA_ID=area.ID AND oilpipe.OILCAN_ID=oilcan.ID AND oil.TYPE='+'\''+oil_type+'\'' 
    print(sql)
    #插入客户表
    sol="insert into customer (phone_num,car_num,id_card) values ("+'\''+cus_p+'\''+','+'\''+cus_c+'\''+','+'\''+cus_id+'\''+")"
    #sol="insert into customer (phonenum,car_num,id_card,register_date) values (%s,%s,%s,%s),[cus_p, cus_c, cus_id, date_str]"
    print(sol)
    #查出客户表id
    sel='select customer.id from customer where phone_num='+'\''+cus_p+'\''+'and car_num='+'\''+cus_c+'\''+'and id_card='+'\''+cus_id+'\''
    
    #把所有的客户信息查出与所插入的客户信息对比
    sal='select customer.phone_num,customer.car_num,customer.id_card from customer'


    #执行查找出相应的鹤位信息
    with connection.cursor() as cursor:
         cursor.execute(sql)
         data = cursor.fetchall()  
         print(data)
         jsonObject=[]
         for row in data:
             result={}
             result['area_name'] =row[0]
             result['oilcan_name']=row[1]
             result['oilpipe_name']=row[2]
             result['price']=row[3]
             jsonObject.append(result)
         print(result)
   
    #判断客户信息存不存在，存在不插入，不存在插入
    with connection.cursor() as cursor2:
        cursor2.execute(sal)
        cus=cursor2.fetchall()
        flag=0
        for i in range(len(cus)):
            #查询出的手机号
            c_phone=cus[i][0]
            #print(c_phone)
            #查询出的车牌号
            c_car=cus[i][1]
            #print(c_car)
            #查询出的身份证号
            c_id=cus[i][2]
            #print(c_id)
            if c_phone == cus_p and c_car == cus_c and c_id == cus_id :
                print("break")
                break
            else:
                print("next")
                flag+=1
            print(flag)
            if flag == len(cus) :
                cursor2.execute(sol)
                print("insert")
           
     #执行插入订单一部分信息
    with connection.cursor() as cursor1:
        #先查询出客户id
         cursor1.execute(sel)
         data1 = cursor1.fetchall()
         print(data1)
         #客户id
         cu_id=str(data1[0][0])
         print(cu_id)
        #插入订单表的一部分信息
        #sql1="insert into order_detail (volumn,ordertime) values ("+'\''+oil_val+'\''+','+'\''+t_date+'\''+")"
         szl="insert into order_detail (volumn,registertime,ordertime,customer_id) values ("+'\''+oil_val+'\''+','+'\''+date_str+'\''+','+'\''+t_date+'\''+','+'\''+cu_id+'\''+")"
         print(szl)
         cursor1.execute(szl)
         zv="insert into customer (id,phone_num,car_num,id_card) values ("+'\''+cu_id+'\''+',''\''+cus_p+'\''+','+'\''+cus_c+'\''+','+'\''+cus_id+'\''+")"
         UDPClient.sendMessage(zv)
    return JsonResponse(jsonObject,safe=False,json_dumps_params={'ensure_ascii': False})


#根数输入的信息生成订单
def makelist(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    area_name=object['area_id']
    oilcan_name=object['oilcan_id']
    oilpipe_name=object['oilpipe_id']
    print(oilpipe_name)
    with connection.cursor() as cursor:
        #查询出更新哪条oilpipe
        swl='select order_detail.id from order_detail'
        cursor.execute(swl)
        data = cursor.fetchall()
        le=str(len(data))
        #更新oilpipeid
        sqp='update order_detail  set oilpipe_id='+'\''+oilpipe_name+'\''+'where order_detail.id='+'\''+le+'\''
        al="insert into order_detail (id,oilpipe_id,volumn,registertime,ordertime,customer_id) values ("+'\''+le+'\''+','+'\''+oilpipe_name+'\''+','+'\''+oil_val+'\''+','+'\''+date_str+'\''+','+'\''+t_date+'\''+','+'\''+cu_id+'\''+")"
        cursor.execute(sqp)
        print(sqp)
        UDPClient.sendMessage(al)
        print(al)
        #transaction.set_dirty()
        #查询出所有需要的订单信息
        sal='select order_detail.id,'\
                                    'customer.PHONE_NUM,'\
                                    'customer.CAR_NUM,'\
                                    'customer.ID_CARD,'\
                                    'order_detail.VOLUMN,'\
                                    'order_detail.REGISTERTIME,'\
                                    'order_detail.OILPIPE_ID,'\
                                    'oilcan.id,'\
                                    'area.ID,'\
                                    'order_detail.`STATUS`,'\
                                    'order_detail.staff_s,'\
                                    'order_detail.ORDERTIME,'\
                                    'order_detail.STARTTIME,'\
                                    'order_detail.FINISHTIME FROM order_detail,customer,oilcan,area,oilpipe where  order_detail.CUSTOMER_ID=customer.ID AND order_detail.OILPIPE_ID=oilpipe.ID AND oilpipe.OILCAN_ID=oilcan.ID AND area.ID=oilcan.AREA_ID order by order_detail.id'
        print(sal)
        cursor.execute(sal)
        deta = cursor.fetchall()
        print (deta)
        jsonObject=[]
        for row in deta:
            result={}
            result['id'] =row[0]
            #print(result['id'])
            result['phone'] =row[1]
            #print(result['phone'])
            result['car'] =row[2]
            result['id_card'] =row[3]
            result['volumn'] =row[4]
            #print(result['volumn'])
            result['reg_time'] =row[5]
            #print(result['reg_time'])
            result['oilpipe_id'] =row[6]
            result['oilcan_id'] =row[7]
            result['area_id'] =row[8]
            result['statu'] =row[9]
            result['sta'] =row[10]
            result['ord_time'] =row[11]
            result['st_time'] =row[12]
            result['fi_time'] =row[13]
            jsonObject.append(result)
        print(jsonObject)
        return JsonResponse(jsonObject,safe=False,json_dumps_params={'ensure_ascii': False})


#查看清单列表
def listshow(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr = request.body
    object = json.loads(jsonstr)
    staff_name = object['staff_name']
    cus_phone = object['cus_phone']
    be_time = object['be_time']
    fi_time = object['fi_time']
    order_state = object['state']
    with connection.cursor() as cursor:
        # 查询出所有需要的订单信息
        spl = 'select order_detail.id,' \
              'customer.PHONE_NUM,' \
              'customer.CAR_NUM,' \
              'customer.ID_CARD,' \
              'order_detail.VOLUMN,' \
              'order_detail.REGISTERTIME,' \
              'order_detail.OILPIPE_ID,' \
              'oilcan.id,' \
              'area.ID,' \
              'order_detail.`STATUS`,' \
              'order_detail.staff_s,' \
              'order_detail.ORDERTIME,' \
              'order_detail.STARTTIME,' \
              'order_detail.FINISHTIME FROM order_detail,customer,oilcan,area,oilpipe where  order_detail.CUSTOMER_ID=customer.ID AND order_detail.OILPIPE_ID=oilpipe.ID AND oilpipe.OILCAN_ID=oilcan.ID AND area.ID=oilcan.AREA_ID '
        print(spl)
        # 条件查询字符串拼接

        if staff_name == '':
            print(staff_name)
        else:
            spl = spl + ' AND order_detail.staff_s= ' + '"' + staff_name + '"'
        if cus_phone == '':
            print(cus_phone)
        else:
            spl = spl + ' AND customer.phone_num= ' + '"' + cus_phone + '"'
        if be_time == '':
            print(be_time)
        else:
            spl = spl + ' AND order_detail.starttime=' + '"' + be_time + '"'
        if fi_time == '':
            print(fi_time)
        else:
            spl = spl + ' AND  order_detail.finishtime=' + '"' + fi_time+ '"'
        if order_state == '':
            print(order_state)
        else:
            spl = spl + ' AND order_detail.status=' + '"' + order_state + '"'
        spl=spl+'order by order_detail.id'



        cursor.execute(spl)
        dta = cursor.fetchall()
        print (dta)
        jsonObject = []
        for row in dta:
            result = {}
            result['id'] = row[0]
            # print(result['id'])
            result['phone'] = row[1]
            # print(result['phone'])
            result['car'] = row[2]
            result['id_card'] = row[3]
            result['volumn'] = row[4]
            # print(result['volumn'])
            result['reg_time'] = row[5]
            # print(result['reg_time'])
            result['oilpipe_id'] = row[6]
            result['oilcan_id'] = row[7]
            result['area_id'] = row[8]
            result['statu'] = row[9]
            result['sta'] = row[10]
            result['ord_time'] = row[11]
            result['st_time'] = row[12]
            result['fi_time'] = row[13]
            jsonObject.append(result)
        print(jsonObject)
        return JsonResponse(jsonObject, safe=False, json_dumps_params={'ensure_ascii': False})









    




    


    




