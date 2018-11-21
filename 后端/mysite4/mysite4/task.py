# -*- coding: utf-8 -*-
 
from django.http import HttpRequest,HttpResponse  
from django.http import JsonResponse  
from json import dumps  
from django.core import serializers  
import json
from django.db import connection

#任务展示
def  getTaskData(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    warning_type=object['warning_type']
    oil_id=object['oil_id']
    area_name=object['area_name']
    oilcan_name=object['oilcan_name']
    begin_time=object['begin_time']
    finish_time=object['finish_time']
    print(object)
    sql='SELECT task.id AS id,task.type AS type,task.`VALUE` AS val,task.oil_id AS oil_id,area.`NAME` AS area_name,oilcan.`NAME` AS oilcan_name,task_manage.begin_time AS begin_time,task_manage.finish_time AS finish_time FROM task,task_manage,oilcan,area WHERE area.id = oilcan.AREA_ID AND oilcan.ID = task.OILCAN_ID AND task_manage.TASK_ID=task.ID AND task.OIL_ID=oilcan.OIL_ID'
    #判断条件是否成立
    print(sql)
    if warning_type == '' :
        print(warning_type)
    else :
        sql=sql+' AND task.type= '+ '"'+warning_type+'"'
    if oil_id == '' :
        print(oil_id)
    else :
        sql=sql+'AND task.oil_id='+'"'+oil_id+'"'
    if area_name == '' :
        print(area_name)
    else :
        sql=sql+' AND area.name='+'"'+area_name+'"'
    if oilcan_name == '' :
        print(oilcan_name)
    else :
        sql=sql+' AND  oilcan.name='+'"'+oilcan_name+'"'
    if begin_time == '' :
        print(begin_time)
    else :
        sql=sql+' AND task_manage.begin_time='+'"'+begin_time+'"'
    if finish_time == '' :
        print(finish_time)
    else :
        sql=sql+finish_time+'"'+'AND task.oil_id='+'"'
    sql=sql+' ORDER BY ID ;'
    print(sql)
 # 使用SQL语句
    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()  
        jsonObj=[]
        for row in data:
            result={}
            result['id'] =row[0]
            result['type']=row[1]
            result['val']=row[2]
            result['oil_id']=row[3]
            result['oilcan_name']=row[4]
            result['area_name']=row[5]
            result['begin_time']=row[6]
            result['finish_time']=row[7]
            jsonObj.append(result)
    return JsonResponse(jsonObj, safe=False, json_dumps_params={'ensure_ascii': False})



#石油ID信息
def getOilData(request,aid):

    with connection.cursor() as cursor:
        cursor.execute("select oil.type,oil.oil_no,oil.price,oil.density  from oil where oil.id="+aid)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result1={}
            result1['type'] =row[0]
            result1['oil_no'] =row[1]
            result1['oil_density'] =row[2]
            result1['oil_price'] =row[3]
            jsonObject.append(result1)
        return JsonResponse(jsonObject,safe=False,json_dumps_params={'ensure_ascii': False})


















