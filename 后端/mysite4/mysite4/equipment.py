# -*- coding: utf-8 -*-
 
from django.http import HttpRequest,HttpResponse  
from django.http import JsonResponse  
from json import dumps  
from django.core import serializers  
import json
from django.db import connection
from . import UDPClient

#实时数据显示
def getEquipment(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    area_name=object['area_name']
    oilcan_name=object['oilcan_name']
    oilpipe_name=object['oilpipe_name']
    print(object)
    #判断条件是否成立
    if area_name == '' or oilcan_name == '' or oilpipe_name == '':
        print(area_name,oilcan_name,oilpipe_name)
    else :
        sql = 'SELECT ' \
              'tab.DEVICE_TYPE,' \
              'tab.DEVICE_ID,' \
              'tab.val,' \
              'tab.MOLD,' \
              'tab.STIME ' \
              'FROM ( ' \
              'SELECT ' \
              'statistics.ID,'\
              'statistics.DEVICE_TYPE,' \
              'statistics.DEVICE_ID,' \
              'statistics.val, ' \
              'statistics.MOLD,' \
              'statistics.STIME ' \
              'FROM ' \
              'statistics,' \
              'device ' \
              'WHERE ' \
              'device.ID = statistics.DEVICE_ID ' \
              'AND device.AREA_ID =' + '\'' + area_name + '\'' + 'AND device.OILCAN_ID = ' + '\'' + oilcan_name + '\'' + ' AND ( device.OILPIPE_ID = ' + '\'' + oilpipe_name + '\'' + ' OR device.OILPIPE_ID = 0 ) ORDER BY statistics.STIME DESC LIMIT 100 ) AS tab GROUP BY tab.DEVICE_ID'
    print(sql)

    ssql = 'SELECT ' \
          'tab.ID,' \
          'tab.DEVICE_TYPE,' \
          'tab.DEVICE_ID,' \
          'tab.val,' \
          'tab.MOLD,' \
          'tab.description,' \
          'tab.STIME ' \
          'FROM ( ' \
          'SELECT ' \
          'statistics.ID,' \
          'statistics.DEVICE_TYPE,' \
          'statistics.DEVICE_ID,' \
          'statistics.val, ' \
          'statistics.MOLD,' \
          'statistics.description,' \
          'statistics.STIME ' \
          'FROM ' \
          'statistics,' \
          'device ' \
          'WHERE ' \
          'device.ID = statistics.DEVICE_ID ' \
          'AND device.AREA_ID =' + '\'' + area_name + '\'' + 'AND device.OILCAN_ID = ' + '\'' + oilcan_name + '\'' + ' AND ( device.OILPIPE_ID = ' + '\'' + oilpipe_name + '\'' + ' OR device.OILPIPE_ID = 0 ) ORDER BY statistics.STIME DESC LIMIT 100 ) AS tab GROUP BY tab.DEVICE_ID'
    print(ssql)
    UDPClient.sendMessage(ssql)
 # 使用SQL语句
    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        jsonObj=[]
        for row in data:
            result={}
            result['device_id'] = row[0]
            result['device_type'] =row[1]
            result['device_val']=row[2]
            result['device_mode']=row[3]
            result['device_time']=row[4]
            jsonObj.append(result)
    print(jsonObj)
    return JsonResponse(jsonObj, safe=False, json_dumps_params={'ensure_ascii': False})



#历史数据展示
def historyList(request):
 # 获取前端条件
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    device_type=object['device_type']
    device_name=object['device_name']
    mold=object['mold']
    desc=object['desc']
    oilpipe_id=object['oilpipe_id']
    time=object['time']
    print(object)
    sql="SELECT statistics.ID,statistics.DEVICE_TYPE,statistics.DEVICE_ID,device.`NAME`,statistics.val,statistics.MOLD,statistics.description,oilpipe.NAME ,statistics.STIME FROM statistics,device,oilpipe where device.TYPE=statistics.DEVICE_TYPE AND device.ID=statistics.DEVICE_ID AND  device.oilpipe_id=oilpipe.id "
    #判断条件是否成立
    if device_type == '' :
        print(device_type)
    else :
        sql=sql+' AND statistics.DEVICE_TYPE= '+ '"'+device_type+'"'
    if device_name == '' :
        print(device_name)
    else :
        sql=sql+' AND device.`NAME`= '+ '"'+device_name+'"'
    if mold == '' :
           print(mold)
    else :
        sql=sql+' AND statistics.MOLD='+'"'+mold+'"'
    if desc == '' :
           print(desc)
    else :
        sql=sql+' AND  statistics.description='+'"'+desc+'"'
    if oilpipe_id == '' :
           print(oilpipe_id)
    else :
        sql=sql+' AND device.OILPIPE_ID='+'"'+oilpipe_id+'"'
    if time == '' :
           print(time)
    else :
        sql=sql+' AND statistics.STIME='+'"'+time+'"'
    sql=sql+' ORDER BY ID ;'
    print(sql)
    with connection.cursor() as cursor:
         cursor.execute(sql)
         data = cursor.fetchall()
         jsonObj=[]
         for row in data:
             result={}
             result['id'] =row[0]
             result['device_type']=row[1]
             result['device_id']=row[2]
             result['device_name']=row[3]
             result['value']=row[4]
             result['mold']=row[5]
             result['desc']=row[6]
             result['oilpipe_id']=row[7]
             result['time']=row[8]
             jsonObj.append(result)
         print(jsonObj)
    return JsonResponse(jsonObj, safe=False, json_dumps_params={'ensure_ascii': False})


#下面开始为各个设备的属性

#温度计
def  th(request):
    with connection.cursor() as cursor:
        sql1='select th.max_value,th.min_value,th.max_warning,th.min_warning from thermometer as th where id=1 '
        cursor.execute(sql1)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result={}
            result['ma_v'] =row[0]
            result['mi_v'] =row[1]
            result['ma_w'] =row[2]
            result['mi_w'] =row[3]
            jsonObject.append(result)
    return JsonResponse(jsonObject, safe=False, json_dumps_params={'ensure_ascii': False})
#液压计
def  pi(request):
    with connection.cursor() as cursor:
        sql1='select pi.max_value,pi.min_value,pi.max_warning,pi.min_warning from piezometer as pi where id=1 '
        cursor.execute(sql1)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result={}
            result['ma_v'] =row[0]
            result['mi_v'] =row[1]
            result['ma_w'] =row[2]
            result['mi_w'] =row[3]
            jsonObject.append(result)
    return JsonResponse(jsonObject, safe=False, json_dumps_params={'ensure_ascii': False})
#流量计
def  fl(request):
    with connection.cursor() as cursor:
        sql1='select fl.max_value,fl.min_value,fl.max_warning,fl.min_warning from flowmeter as fl where id=1 '
        cursor.execute(sql1)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result={}
            result['ma_v'] =row[0]
            result['mi_v'] =row[1]
            result['ma_w'] =row[2]
            result['mi_w'] =row[3]
            jsonObject.append(result)
    return JsonResponse(jsonObject, safe=False, json_dumps_params={'ensure_ascii': False})















