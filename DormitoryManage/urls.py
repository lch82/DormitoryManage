"""DormitoryManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
#from dormitory import views #测试hello添加该行
from django.views.generic.base import TemplateView #vue添加该行
from rbac import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('index/',views.hello), #测试hello添加该行
    #path('',TemplateView.as_view(template_name="index.html")),
    path('login/', views.login,name='login'), #首页（登录）
    path('logout/', views.logout,name='logout'), #退出登录
    path('student/',views.student_index,name='Student'),
    path('monitor/',views.monitor_index),
    path('leader/',views.leader_index),
    path('teacher/',views.teacher_index),
    path('housemaster/',views.housemaster_index),
    path('housemaster/search/',views.HousemasterIndex.search,name='HousemasterSearch'),
    path('housemaster/statistic/',views.HousemasterIndex.statistic,name='HousemasterStatistic'),
    path('teacher/search/',views.TeacherIndex.search,name='TeacherSearch'),
    path('teacher/statistic/',views.TeacherIndex.statistic,name='TeacherStatistic'),
    path('leader/show1/',views.LeaderIndex.show,name='LeaderShow'),
    path('leader/show2/',views.LeaderIndex.show1,name='LeaderShow1'),
    path('leader/search/',views.LeaderIndex.search,name='LeaderSearch'),
    path('leader/statistic/',views.LeaderIndex.statistic,name='LeaderStatistic'),
    path('leader/statistic-info/',views.LeaderIndex.statisticinfo,name='LeaderStatisticInfo'),
    path('monitor/check/',views.MonitorIndex.monitorcheck,name='MonitorCheck'),
    path('monitor/editinfoshow/',views.MonitorIndex.editinfoshow,name='EditInfoShow'),
    path('monitor/edit/',views.MonitorIndex.monitoredit,name='MonitorEdit'),
    path('monitor/inform/',views.MonitorIndex.informshow,name='MonitorInform'),
    path('monitor/informsuccess/',views.MonitorIndex.monitorinform,name='MonitorInformSuccess'),
]
