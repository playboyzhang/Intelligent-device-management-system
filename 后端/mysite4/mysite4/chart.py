# -*- coding: utf-8 -*-

from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
from django.core import serializers
import json, string
from django.db import connection, transaction

from datetime import datetime
def line (request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    area_name=object['area_name']
    oilcan_name=object['oilcan_name']
    oilpipe_name=object['oilpipe_name']
    date_time = object['date_time']
    print(object)
    sql='SELECT ' \
        'statistics.DEVICE_ID,' \
        'statistics.VAL,' \
        'statistics.STIME ' \
        'FROM ' \
        'statistics,' \
        'device ' \
        'WHERE ' \
              'device.ID = statistics.DEVICE_ID  '\
              'AND device.AREA_ID =' + '\'' + area_name + '\'' + 'AND device.OILCAN_ID = ' + '\'' + oilcan_name + '\'' + ' AND ( device.OILPIPE_ID = ' + '\'' + oilpipe_name + '\'' + ' OR device.OILPIPE_ID = 0 )'+'AND statistics.DEVICE_TYPE <> \'gnd\' AND statistics.DEVICE_TYPE <> \'oilleak\' AND STIME BETWEEN DATE_FORMAT('+'\''+date_time+'\''+',\'%Y-%m-%d 00:00:00\')  and '+'\''+date_time+'\''+'  ORDER BY statistics.DEVICE_ID,STIME ASC'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        jsonObj = []
        for row in data:
            result = {}
            result['device_id'] = row[0]
            result['val'] = row[1]
            result['stime'] = row[2]
            jsonObj.append(result)
    print(jsonObj)
    return JsonResponse(jsonObj, safe=False, json_dumps_params={'ensure_ascii': False})



def columnar(request):
    sal='SELECT ' \
        'oil.TYPE,' \
        'sum(order_detail.VOLUMN), ' \
        'DATE_FORMAT(order_detail.ORDERTIME, '+ '\' %Y-%m-%d \'' +') AS time '\
        'FROM ' \
        'order_detail,  ' \
        'oilpipe, ' \
        'oil, ' \
        'oilcan ' \
        'where order_detail.OILPIPE_ID=oilpipe.ID AND oilpipe.OILCAN_ID=oilcan.ID AND oilcan.OIL_ID=oil.ID GROUP BY time,oil.TYPE DESC'
    with connection.cursor() as cursor:
        cursor.execute(sal)
        data = cursor.fetchall()
        jsonObj = []
        for row in data:
            result = {}
            result['type'] = row[0]
            result['sum'] = row[1]
            result['oil_time'] = row[2]
            jsonObj.append(result)
    print(jsonObj)
    return JsonResponse(jsonObj, safe=False, json_dumps_params={'ensure_ascii': False})
