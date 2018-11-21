# -*- coding: utf-8 -*-
 
from django.http import HttpRequest,HttpResponse  
from django.http import JsonResponse  
from json import dumps  
from django.core import serializers  
import json
from django.db import connection
#报警展示
def getDangerData(request):
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
    sql="SELECT statistics.ID,statistics.DEVICE_TYPE,statistics.DEVICE_ID,device.`NAME`,statistics.val,statistics.MOLD,statistics.description,oilpipe.NAME ,statistics.STIME FROM statistics,device,oilpipe where device.TYPE=statistics.DEVICE_TYPE AND device.ID=statistics.DEVICE_ID AND  device.oilpipe_id=oilpipe.id AND statistics.MOLD<> 'normal'"
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
        sql=sql+' AND statistics.STIME like DATE_FORMAT('+'\''+time+'\''+','+'\''+'%Y-%m-%d %%:%%:%% '+'\')'
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


















