# -*- coding: utf-8 -*-
 
from django.http import HttpRequest,HttpResponse  
from django.http import JsonResponse  
from json import dumps  
from django.core import serializers  
import json
from django.db import connection


# 针对设备的数据库操作
 

#获取设备列表
def getDeviceList(request):
    with connection.cursor() as cursor:
        sql="SELECT device.ID,device.TYPE,device. NAME,area. NAME,oilcan. NAME,oilpipe. NAME FROM device,oilcan,oilpipe,area WHERE device.OILCAN_ID = oilcan.ID AND device.OILPIPE_ID = oilpipe.ID AND device.AREA_ID = area.ID AND  device.type<>'oilleak' AND device.type<>'gnd'"
        cursor.execute(sql)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result={}
            result['id'] =row[0]
            result['device_type'] =row[1]
            result['device_id'] =row[2]
            result['area_id'] =row[3]
            result['oilcan_id'] =row[4]
            result['oilpipe_id'] =row[5]
            jsonObject.append(result)
        return JsonResponse(jsonObject,safe=False,json_dumps_params={'ensure_ascii': False})

#获取设备对应的ID
def getDevice(request,aid):
    sql1='SELECT device.ID,device.TYPE,device. NAME,area.id,oilcan.id,oilpipe.id FROM device,oilcan,oilpipe,area WHERE device.OILCAN_ID = oilcan.ID AND device.OILPIPE_ID = oilpipe.ID AND device.AREA_ID = area.ID AND device.id='+aid
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result1={}
            result1['id'] =row[0]
            result1['device_type'] =row[1]
            result1['device_id'] =row[2]
            result1['area_id'] =row[3]
            result1['oilcan_id'] =row[4]
            result1['oilpipe_id'] =row[5]
            jsonObject.append(result1)
        print(jsonObject)
        return JsonResponse(jsonObject,safe=False,json_dumps_params={'ensure_ascii': False})




#更新设备
def updateDevice(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    id=object['id']
    device_type=object[u'device_type']
    device_id=object['device_id']
    area_id=object['area_id']
    oilcan_id=object['oilcan_id']
    oilpipe_id=object['oilpipe_id']
    print(object)
    #更新操作
    with connection.cursor() as cursor:
        sql2='update device set device.AREA_ID='+'\''+area_id+'\'' +',device.oilcan_id='+'\''+oilcan_id+'\''+',device.oilpipe_id='+'\''+oilpipe_id+'\''+' where device.id='+'\''+id+'\''
        print(sql2)
        cursor.execute(sql2)
        data = cursor.fetchall()
        print (data)
        return HttpResponse("更新成功")     


#设备清单页数
def page1(request):
        with connection.cursor() as cursor:
            sql = "SELECT device.ID,device.TYPE,device. NAME,area. NAME,oilcan. NAME,oilpipe. NAME FROM device,oilcan,oilpipe,area WHERE device.OILCAN_ID = oilcan.ID AND device.OILPIPE_ID = oilpipe.ID AND device.AREA_ID = area.ID AND  device.type<>'oilleak' AND device.type<>'gnd'"
            cursor.execute(sql)
            data = cursor.fetchall()
            print (data)
            datalen = len(data)
            print(datalen)
            res={'datalen':datalen}
            return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})