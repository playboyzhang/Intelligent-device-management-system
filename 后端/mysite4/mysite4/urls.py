"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
'''from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]'''
from django.conf.urls import url
#from django.conf.urls import patterns, include, url
from . import Users,devicedb,danger,chart,equipment,service
from django.contrib import admin
#from login import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^userList$',Users.getUserList),
    url(r'^getUser/(\d+)$',Users.getUser),
    url(r'^deleteUser/(\d+)$',Users.deleteUser),
    url(r'^addUser$',Users.addUser),
    url(r'^updateUser$',Users.updateUser),
    #url(r'^login/',views.login, name='login'),
    url(r'^deviceList$',devicedb.getDeviceList),
    url(r'^getDevice/(\d+)$',devicedb.getDevice),
    url(r'^updateDevice$',devicedb.updateDevice),
    url(r'^getDangerData$',danger.getDangerData),
    url(r'^getEquipment$',equipment.getEquipment),
    url(r'^historyList$',equipment.historyList),
    url(r'^freeoilpipe$',service.freeoilpipe),
    url(r'^makelist$',service.makelist),
    url(r'^listshow$',service.listshow),
    url(r'^land$',Users.land),
    url(r'^getrole$',Users.getrole),
    url(r'^deleterole/(\d+)$',Users.deleterole),
    url(r'^addrole$',Users.addrole),
    url(r'^columnar$',chart.columnar),
    url(r'^line$',chart.line),
    url(r'^page1$',devicedb.page1),
    url(r'^th$',equipment.th),
    url(r'^pi$',equipment.pi),
    url(r'^fl$',equipment.fl),
]