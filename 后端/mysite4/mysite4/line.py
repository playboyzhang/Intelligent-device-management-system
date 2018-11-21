# -*- coding: utf-8 -*-
 
from django.http import HttpRequest,HttpResponse  
from django.http import JsonResponse  
from json import dumps  
from django.core import serializers  
from login.models import Device
import json


# 针对设备的数据库操作
 

#获取设备列表
def getDeviceList(request):
    responses = ""
    list = Device.objects.all()
    response1 = serializers.serialize('json',list)
    print (response1)
    return HttpResponse(response1)

#获取设备对应的ID
def getDevice(request,aid):
    list=Device.objects.filter(id = aid)
    print(aid)
    response1 = serializers.serialize('json',list)
    print (response1)
    return HttpResponse(response1)

#删除设备
def deleteDevice(request,deleteId):
    Device.objects.get(id=deleteId).delete()
    return HttpResponse("delete success!")

#添加设备
def addDevice(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body.decode()
    print (jsonstr)
    object=json.loads(jsonstr)
    print(object)
    print(object['D_name'])
    #增加操作
    d_name=Device(D_id=object['D_id'],D_name=object['D_name'],D_type=object['D_type'])
    d_name.save()
    return HttpResponse("测试新增，使用POST")

#更新设备
def updateDevice(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body.decode()
    print (jsonstr)
    object=json.loads(jsonstr)
    up=Device.objects.get(id=object['id'])
    up.D_id=object['D_id']
    up.D_name=object['D_name']
    up.D_type=object['D_type'] 
    up.save()
    return HttpResponse("测试修改，使用POST")   