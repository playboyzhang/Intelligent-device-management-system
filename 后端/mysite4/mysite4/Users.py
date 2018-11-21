# -*- coding: utf-8 -*-
 
from django.http import HttpRequest,HttpResponse  
from django.http import JsonResponse  
from json import dumps  
from django.core import serializers  
import json
from django.db import connection
#from django.db.transaction import TransactionManagementError
# 数据库操作
from . import UDPClient#导入客户端
from datetime import datetime
 

#获取用户列表
def getUserList(request):
    with connection.cursor() as cursor:
        sql1='select staff.id,staff.account,staff.name,staff.phonenum,role.type,staff.password,staff.date from staff,role where role.id=staff.session '
        cursor.execute(sql1)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        data_len=len(data)
        print(data_len)
        for row in data:
            result={}
            result['id'] =row[0]
            result['account'] =row[1]
            result['name'] =row[2]
            result['phonenum'] =row[3]
            result['role_type'] = row[4]
            result['password'] =row[5]
            result['staff_date'] =row[6]
            jsonObject.append(result)
        #UDPClient.sendMessage(sql1)
        #发送至UDP服务器
        #print(state)
        return JsonResponse(jsonObject, safe=False, json_dumps_params={'ensure_ascii': False})
    #print u'执行发送...'
    #message = 'select staff.id,staff.account,staff.name,staff.phonenum,staff.area_no,staff.password,staff.staff_type,staff.date from staff'
    #state = UDPClient.sendMessage(message)  # 发送至UDP服务器
    #print state
    #if isinstance(state, unicode):
    #    state = state.encode('utf-8')
    #return HttpResponse("<html>发送状态：<b>{0}</b></html>".format(state))



#获取对应用户id的设备信息
def getUser(request,aid):
    with connection.cursor() as cursor:
        cursor.execute('select staff.id,staff.account,staff.name,staff.phonenum,role.type,staff.password,staff.date from staff,role where role.id=staff.session AND staff.id='+aid)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result1={}
            result1['id'] =row[0]
            result1['account'] =row[1]
            result1['name'] =row[2]
            result1['phonenum'] =row[3]
            result1['role_type'] = row[4]

            result1['password'] = row[5]
            result1['staff_date'] = row[6]
            jsonObject.append(result1)
        print(jsonObject)
        return JsonResponse(jsonObject,safe=False,json_dumps_params={'ensure_ascii': False})

#删除用户
def deleteUser(request,deleteId):
    with connection.cursor() as cursor:
        cursor.execute('delete from staff where staff.id='+deleteId)
        data = cursor.fetchall()
        print (data)
    return HttpResponse("delete success!")

#添加用户
def addUser(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    account=object['account']
    name=object['name']
    password=object['password']
    phonenum=object['phonenum']
    area_no=object['area_no']
    role_type=object['role_type']
    #date=object['staff_date']
    date=datetime.now()
    print(object)
    date_str=datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
    #增加操作
    with connection.cursor() as cursor:
        sql="INSERT INTO staff (account,name,phonenum,area_no,password,date)  VALUES ("+'\''+account+'\''+','+'\''+name+'\''+','+'\''+phonenum+'\''+','+'\''+area_no+'\''+','+'\''+password+'\''+','+'\''+date_str+'\''+")"
        #cursor.execute('INSERT INTO staff (account,name,phonenum,area_no,password,staff_type,date)  VALUES ()')
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        print (data)
        #transaction.commit_unless_managed()
    return HttpResponse("测试新增，使用POST")

#更新用户
def updateUser(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
  
    object=json.loads(jsonstr)
    id=object['id']
    account=object[u'account']
    name=object[u'name']
    password=object[u'password']
    phonenum=object[u'phonenum']
    area_no=object[u'area_no']
    #staff_type=object[u'staff_type']
    print(object)
    #更新操作
    with connection.cursor() as cursor:
        sql1='update staff set staff.account='+'\''+account+'\'' +',staff.name='+'\''+name+'\''+',staff.password='+'\''+password+'\''+',staff.phonenum='+'\''+phonenum+'\''+',staff.area_no='+'\''+area_no+'\''+' where staff.id='+'\''+id+'\''
        print(sql1)
        cursor.execute(sql1)
        data = cursor.fetchall()
        print (data)
        return HttpResponse("测试修改，使用POST")
#获取角色列表
def getrole(response):
    with connection.cursor() as cursor:
        swl='select role.id,role.type from role  '
        cursor.execute(swl)
        data = cursor.fetchall()
        print (data)
        jsonObject=[]
        for row in data:
            result={}
            result['id'] =row[0]
            result['role_type'] =row[1]
            jsonObject.append(result)
    return JsonResponse(jsonObject,safe=False,json_dumps_params={'ensure_ascii': False})


#删除角色
def deleterole(request,deleteId):
    with connection.cursor() as cursor:
        cursor.execute('delete from role where role.id='+deleteId)
        data = cursor.fetchall()
        print (data)
    return HttpResponse("delete success!")

#添加角色
def addrole(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    role_type=object['role_type']
    print(object)
    #增加操作
    with connection.cursor() as cursor:
        sql="INSERT INTO role (type)  VALUES ("+'\''+role_type+'\''+")"
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        print (data)
        #transaction.commit_unless_managed()
    return HttpResponse("测试新增，使用POST")



#用户登录验证
def land(request):
    if request.method == 'POST':
        print(request.body)
    jsonstr=request.body
    object=json.loads(jsonstr)
    user_name=object['username']
    user_password=object['userpassword']
    with connection.cursor() as cursor:
        sql6='select staff.account,staff.password,staff.id,staff.session,staff.name from staff'
        cursor.execute(sql6)
        data = cursor.fetchall()
        #data_len=len(data)
        #data_len=data_len-1
        print(data)
        print(len(data))
        
    for i in range(len(data)):
        account=data[i][0]
        password=data[i][1]
        id=data[i][2]
        session=data[i][3]
        username=data[i][4]
            #for row in data:
            #    print(row)
            #    account=row[0]
            #    password=row[1]
        print(account)
        print(password)
        #print(i)
        #print(len(data))
        #print(data[2][0])
        #print(data[3][1])
        #print(i)
        #print(len(data))
            #for i in range(0,data_len-1):
            #    print(account)
        if(user_name==account and user_password==password ):
            print("succes")
            result={'id':id, 'session':session,'account':username}
            print(result)
            return HttpResponse(json.dumps(result))
        else :
            print("fail")
    return HttpResponse("登录成功！")