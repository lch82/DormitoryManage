from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext

#from rbac.service import initial_session
from rbac import service
from rbac.service import permissions
#from dormitory.models import dormitory,department,student
from rbac.models import dormitory,department,student,teacher
from django.contrib import auth
from django.views.generic.base import View
from django.core.mail import send_mail
from django.contrib import messages
import requests
import time
from twilio.rest import Client # 需要装twilio库
# Create your views here.
""" def hello(request):
    return HttpResponse('Hello,world!') """
message_ls={}
#登陆函数
def login(request):
    if  request.method=="POST":   #发送登录请求
        username=request.POST.get("user")
        pwd=request.POST.get("pwd")
        print("username:",username)
        print("pwd:",pwd)
        #获取Account表里面去找有没有当前的用户名和密码
        user=student.objects.filter(sno=username,spass=pwd).first()
        #select * from student where sno='username' and spass='pwd'
        #select * from student where sno='170400520' or '3'='3'
        print("user: ",user)
        if user:   #如果该用户存在
            if user.sno==username and user.spass==pwd: #SQL注入防御：查询出来的结果再和用户名密码比较如果一致则是正常登陆，不一致认为是攻击
            ############################### 在session中注册用户ID######################
                request.session["user_id"]=user.pk
                #调用组件：获取当前用户所在的所有角色拥有的权限
                permissions.initial_session(user,request)   
                request.session['username'] = user.sno
                print("********")
                print(request.session['permission_dict'])
                print("********")
                url=request.session['permission_dict']
                print('url[0]: ',url[0])
                return redirect(url[0])
        else:
            print("进入这里！")
            user=teacher.objects.filter(tno=username,spass=pwd).first()
            print("user::",user)
            if user:   #如果该用户存在
            ############################### 在session中注册用户ID######################
                request.session["user_id"]=user.pk
            #调用组件：获取当前用户所在的所有角色拥有的权限
                permissions.initial_session(user,request)   
                request.session['username'] = user.tno
                print("********")
                print(request.session['permission_dict'])
                print("********")
                url=request.session['permission_dict']
                print('url[0]: ',url[0])
                return redirect(url[0])

    return render(request,"login.html")
            #跳转到列表页面
            #return redirect("/login/index/")
    #主页（登录）
    #return render(request,"login.html")

#退出函数
def logout(request):
    auth.logout(request)
    return render(request,"login.html")
#学工领导主页
def leader_index(request):   
    #ret = dormitory.objects.all() #宿舍信息
    #在前端页面显示用户名
    #print(request.actions)
    #per = Per(request.actions) 

    return render(request, 'leader.html', locals())

#学生主页
def student_index(request):  
    print("username: ",request.session['username'])
    global messages_ls
    print("**message_ls: ",message_ls)
    ls=message_ls
    print("**ls:",ls)
    stu_sno=request.session['username']
    stu_list=student.objects.filter(sno=stu_sno)
    stu = stu_list[0]
    if stu:
        sdept = department.objects.get(id = stu.sdept_id)
        stu_dept = sdept.dept_name
        stu_class=stu.sclass
        stu_name=stu.name
        stu_dno=stu.dno 
        dorm = dormitory.objects.get(dno = stu_dno)
        stu_dorm_cont=dorm.content
        stu_email=stu.email 
        stu_phone=stu.phone
        text=dorm.text
    global messages_ls
    for k,v in ls.items():
        if k == stu_sno:
            #messages.success(request,v)
            print("k,v: ",k,v)
            messages.success(request,v)
            #return render(request,'student.html',locals(),{'script': "alert", 'msg0': u"注册成功"}) 
            #del messages_ls[k] 
    return render(request,'student.html',locals())

#学生干部主页
def monitor_index(request):
    return render(request,'monitor.html',locals())

#楼长主页
def housemaster_index(request):
    return render(request,'housemaster.html',locals())

#辅导员主页
def teacher_index(request):
    return render(request,'teacher.html',locals())

class HousemasterIndex(View):
    def search(request):
        hm_tno=request.session['username']  #得到楼长的用户名
        hm_list=teacher.objects.filter(tno=hm_tno) #根据教工表得到该用户名的楼长
        hm = hm_list[0] #取符合的第一条记录
        if hm:
            hm_num=hm.sclass #得到管理的楼号
            dorm = dormitory.objects.filter(num=hm_num)  #在宿舍表根据楼号得到所有该楼的宿舍
        return render(request,'housemaster-search.html',locals())
    def statistic(request):
        hm_tno=request.session['username']  #得到楼长的用户名
        hm_list=teacher.objects.filter(tno=hm_tno) #根据教工表得到该用户名的楼长
        hm = hm_list[0] #取符合的第一条记录
        if hm:
            hm_num=hm.sclass #得到管理的楼号
            dorm = dormitory.objects.filter(num=hm_num)  #在宿舍表根据楼号得到所有该楼的宿舍
        d1=[] #优-寝室
        d2=[] #良-寝室
        d3=[] #中-寝室
        d4=[] #及格-寝室
        d5=[] #不及格-寝室
        for i in dorm:
            if i.content=='优':
                d1.append(i.dno)
            if i.content=='良':
                d2.append(i.dno)
            if i.content=='中':
                d3.append(i.dno)
            if i.content=='及格':
                d4.append(i.dno)
            if i.content=='不及格':
                d5.append(i.dno)
        print("d1: ",d1)
        print("d2: ",d2)
        print("d3: ",d3)
        print("d4: ",d4)
        print("d5: ",d5)
        d1_num=len(d1)
        d2_num=len(d2)
        d3_num=len(d3)
        d4_num=len(d4)
        d5_num=len(d5)
        d_num={'d1_num':d1_num,'d2_num':d2_num,'d3_num':d3_num,'d4_num':d4_num,'d5_num':d5_num}
        print("d_num: ",d_num)
        return render(request,'housemaster-statistic.html',locals())

class TeacherIndex(View):
    def search(request):
        th_tno=request.session['username']  #得到用户名
        th_list=teacher.objects.filter(tno=th_tno) #根据教工表得到该用户名的辅导员
        th = th_list[0] #取符合的第一条记录
        if th:
            th_sclass=th.sclass #得到管理的年级
            dorm = dormitory.objects.filter(sclass=th_sclass)  #在宿舍表根据年级得到所有该年级的宿舍
        return render(request,'teacher-search.html',locals())
    def statistic(request):
        th_tno=request.session['username']  #得到用户名
        th_list=teacher.objects.filter(tno=th_tno) #根据教工表得到该用户名的辅导员
        th = th_list[0] #取符合的第一条记录
        if th:
            th_sclass=th.sclass #得到管理的年级
            dorm = dormitory.objects.filter(sclass=th_sclass)  #在宿舍表根据年级得到所有该年级的宿舍
        d1=[] #优-寝室
        d2=[] #良-寝室
        d3=[] #中-寝室
        d4=[] #及格-寝室
        d5=[] #不及格-寝室
        for i in dorm:
            if i.content=='优':
                d1.append(i.dno)
            if i.content=='良':
                d2.append(i.dno)
            if i.content=='中':
                d3.append(i.dno)
            if i.content=='及格':
                d4.append(i.dno)
            if i.content=='不及格':
                d5.append(i.dno)
        print("d1: ",d1)
        print("d2: ",d2)
        print("d3: ",d3)
        print("d4: ",d4)
        print("d5: ",d5)
        d1_num=len(d1)
        d2_num=len(d2)
        d3_num=len(d3)
        d4_num=len(d4)
        d5_num=len(d5)
        d_num={'d1_num':d1_num,'d2_num':d2_num,'d3_num':d3_num,'d4_num':d4_num,'d5_num':d5_num}
        print("d_num: ",d_num)
        return render(request,'teacher-statistic.html',locals())

class LeaderIndex(View):
    def show(request):
        depart = department.objects.filter() #查找时有哪些学院
        return render(request,'leader-search.html',locals())
    
    def show1(request):
        depart = department.objects.filter() #查找时有哪些学院
        return render(request,'leader-statistic.html',locals())

    def search(request):
        depart = department.objects.filter() #查找时有哪些学院
        print(department)
        deptname = request.GET.get('depart')  #获取学院名称
        stu_sclass = request.GET.get('sclass') #获取年级
        print("学院名称： ",deptname)

        if deptname == 'all': #搜索全部学院
            dorm=dormitory.objects.filter()
            name=[]
            for i in dorm:
                temp=i.num
                temp_ls=department.objects.filter(num=temp)
                temp_ls=temp_ls[0]
                name.append(temp_ls.dept_name)
                hebin=list(zip(name,dorm))
            if stu_sclass: 
                dorm = dormitory.objects.filter(sclass=stu_sclass) #找到该年级的所有宿舍
                print("dorm: ",dorm)
                name=[]
                for i in dorm:
                    temp=i.num
                    print("temp:  ",temp)
                    temp_ls=department.objects.filter(num=temp)
                    temp_ls=temp_ls[0]
                    print("temp_ls:",temp_ls)
                    print("type(temp_ls): ",type(temp_ls))
                    print("temp_ls.dept_name: ",temp_ls.dept_name)
                    name.append(temp_ls.dept_name)
                    hebin=list(zip(name,dorm))
                    print("hebin: ",hebin)
                    for a in hebin:
                        for b in a:
                            print(b)
        else: #有选择的学院，则按学院查
            dept_list = department.objects.filter(dept_name=deptname) #在学院表根据名称找到该学院的记录
            print("****到这*****")
            dept=dept_list[0] #取符合的第一条记录
            print("**dept**: ",dept)
            if dept:
                dept_num=dept.num   #得到学院编号
                print("学院编号： ",dept_num)
                dorm = dormitory.objects.filter(num=dept_num)
                print("dorm: ",dorm)
                name=[]
                for i in dorm:
                    temp=i.num                    
                    temp_ls=department.objects.filter(num=temp)
                    temp_ls=temp_ls[0]
                    print("temp_ls:",temp_ls)
                    print("type(temp_ls): ",type(temp_ls))
                    print("temp_ls.dept_name: ",temp_ls.dept_name)
                    name.append(temp_ls.dept_name)
                    hebin=list(zip(name,dorm)) #得到该学院的所有宿舍
                    if stu_sclass: #不仅查看学院，还查看年级_遍历在新的列表操作，删除是在原来的列表操作
                        print("stu_sclass: ",stu_sclass)
                        tt=hebin[:]
                        for ll in hebin:
                            if ll[1].sclass != stu_sclass:
                                print("ll[1].sclass: ",ll[1].sclass)
                                tt.remove(ll)
                        hebin=tt
                        print("筛选后的hebin： ",hebin)
        return render(request,'leader-search.html',locals())

    def statistic(request):
        depart = department.objects.filter() #查找时有哪些学院
        print(department)
        deptname = request.GET.get('depart')  #获取学院名称
        stu_sclass = request.GET.get('sclass') #获取年级
        request.session['deptname']=deptname
        request.session['stu_sclass']=stu_sclass
        print("学院名称： ",deptname)
        d1=[] #优-寝室
        d2=[] #良-寝室
        d3=[] #中-寝室
        d4=[] #及格-寝室
        d5=[] #不及格-寝室
        if deptname == 'all': #搜索全部学院
            dorm=dormitory.objects.filter()
            name=[]
            for i in dorm:
                temp=i.num
                temp_ls=department.objects.filter(num=temp)
                temp_ls=temp_ls[0]
                name.append(temp_ls.dept_name)
                hebin=list(zip(name,dorm))
            if stu_sclass: 
                dorm = dormitory.objects.filter(sclass=stu_sclass) #找到该年级的所有宿舍
                print("dorm: ",dorm)
                name=[]
                for i in dorm:
                    temp=i.num
                    print("temp:  ",temp)
                    temp_ls=department.objects.filter(num=temp)
                    temp_ls=temp_ls[0]
                    print("temp_ls:",temp_ls)
                    print("type(temp_ls): ",type(temp_ls))
                    print("temp_ls.dept_name: ",temp_ls.dept_name)
                    name.append(temp_ls.dept_name)
                    hebin=list(zip(name,dorm))
                    print("hebin: ",hebin)
                    for a in hebin:
                        for b in a:
                            print(b)
        else: #有选择的学院，则按学院查
            dept_list = department.objects.filter(dept_name=deptname) #在学院表根据名称找到该学院的记录
            print("****到这*****")
            dept=dept_list[0] #取符合的第一条记录
            print("**dept**: ",dept)
            if dept:
                dept_num=dept.num   #得到学院编号
                print("学院编号： ",dept_num)
                dorm = dormitory.objects.filter(num=dept_num)
                print("dorm: ",dorm)
                name=[]
                for i in dorm:
                    temp=i.num                    
                    temp_ls=department.objects.filter(num=temp)
                    temp_ls=temp_ls[0]
                    print("temp_ls:",temp_ls)
                    print("type(temp_ls): ",type(temp_ls))
                    print("temp_ls.dept_name: ",temp_ls.dept_name)
                    name.append(temp_ls.dept_name)
                    hebin=list(zip(name,dorm)) #得到该学院的所有宿舍
                    if stu_sclass: #不仅查看学院，还查看年级_遍历在新的列表操作，删除是在原来的列表操作
                        print("stu_sclass: ",stu_sclass)
                        tt=hebin[:]
                        for ll in hebin:
                            if ll[1].sclass != stu_sclass:
                                print("ll[1].sclass: ",ll[1].sclass)
                                tt.remove(ll)
                        hebin=tt
                        print("筛选后的hebin： ",hebin)
        for j in hebin:
            if j[1].content=='优':
                d1.append(j[1].dno)
            if j[1].content=='良':
                d2.append(j[1].dno)
            if j[1].content=='中':
                d3.append(j[1].dno)
            if j[1].content=='及格':
                d4.append(j[1].dno)
            if j[1].content=='不及格':
                d5.append(j[1].dno)
        request.session['d1']=d1
        request.session['d2']=d2
        request.session['d3']=d3
        request.session['d4']=d4
        request.session['d5']=d5
        d1_num=len(d1)
        d2_num=len(d2)
        d3_num=len(d3)
        d4_num=len(d4)
        d5_num=len(d5)
        d_num={'d1_num':d1_num,'d2_num':d2_num,'d3_num':d3_num,'d4_num':d4_num,'d5_num':d5_num}
        request.session['d_num']=d_num
        print("d_num: ",d_num)
        return render(request,'leader-statistic.html',locals())
    def statisticinfo(request):
        deptname=request.session['deptname']
        stu_sclass=request.session['stu_sclass']
        d1=request.session['d1']
        d2=request.session['d2']
        d3=request.session['d3']
        d4=request.session['d4']
        d5=request.session['d5']
        d_num=request.session['d_num']
        return render(request,'leader-statistic-info.html',locals())

class MonitorIndex(View):
    def informshow(request):
        m_sno=request.session['username']  #得到用户名
        mm_list=student.objects.filter(sno=m_sno) #根据学生表得到该用户名的学生干部
        mm = mm_list[0] #取符合的第一条记录
        if mm:
            m_deptid=mm.sdept_id #得到管理的学院编号
            print("m_dept: ",m_deptid)
            dept = department.objects.filter(id=m_deptid)#找该学员编号对应的学院记录
            print("dept: ",dept)
            mm_dept=dept[0] #取第一条记录
            mm_name=mm_dept.dept_name
            print("mm_name: ",mm_name)
            mm_num=mm_dept.num
            print("mm_num: ",mm_num)
            dorm = dormitory.objects.filter(num=mm_num)  #在宿舍表根据学院楼号得到所有该学院的宿舍
        dorm_ls=[]#所有不及格的寝室
        email_dict={}  #邮箱字典“宿舍号：邮箱”
        stu_dict={}  #学生字典“宿舍号：学号”     与邮箱字典一一对应
        for i in dorm:
            if i.content=="不及格":
                dorm_ls.append(i)    
                key=i.dno   #该不及格寝室的号码
                print("dno: ",key)
                stu_ls = student.objects.filter(dno=key)  #该不及格寝室的学生
                for j in stu_ls:  
                    value=j.email
                    email_dict.setdefault(key,[]).append(value)
                    value2=j.sno
                    stu_dict.setdefault(key,[]).append(value2)
        """ print("email_dict: ",email_dict)
        for k,m in email_dict.items():
            print("k:",k)
            print("m:",m)
            for l in m:
                print("l:",l)

        print("stu_dict: ",stu_dict)
        for k,m in stu_dict.items():
            print("k:",k)
            print("m:",m)
            for l in m:
                print("l:",l) """
        return render(request,'monitor-inform.html',locals())
    
    def monitorinform(request):
        dno = request.GET.get('dno')
        num = request.GET.get('num')
        depart=department.objects.filter(num=num)
        dept=depart[0]
        dept_name=dept.dept_name

        dorm=dormitory.objects.filter(dno=dno,num=num)
        dorm_temp=dorm[0]
        dorm_text=dorm_temp.text
        
        title="寝室卫生管理系统———任务通知提醒"
        text="宿舍楼："+num+", 寝室："+dno+"， 卫生检查不及格，整改方案为："+dorm_text+"。"
        print("text:",text)
        email_from="wenqiwang2020@163.com"

        email_ls=[]  #邮箱列表“邮箱”
        sno_ls=[]  #学号列表“学号”     与邮箱列表一一对应
        phone_ls=[] #电话号码列表
        stu_ls = student.objects.filter(dno=dno)  #该不及格寝室的学生
        global message_ls
        #message_ls={}
        for i in stu_ls:
            sno=i.sno
            email=i.email
            phone=i.phone
            sno_ls.append(sno)
            email_ls.append(email)
            phone_ls.append(phone)
            message_ls[sno]=text
        print("sno_ls:",sno_ls)
        print("email_ls:",email_ls)
        print("phone_ls:",phone_ls)
        print("message_ls: ",message_ls)
        #邮件通知
        send_mail(title, text, email_from,email_ls, fail_silently=False)
        print("成功！")
        #短信通知
        for j in phone_ls:
            if j:
                send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                account_sid = 'AC8bd2f54acc0607c8b460cea4f58220db' # api参数 复制粘贴过来
                auth_token = '1f2d50389191af8a6059123995e39ef9' # api参数 复制粘贴过来
                client = Client(account_sid, auth_token) # 账户认证
                message = client.messages.create(
                to="+8615065843219", # 接受短信的手机号 注意写中国区号 +86
                from_="+18704104197", # api参数 Number(领取的虚拟号码
                body=text) #自定义短信内容
                print('接收短信号码：'+message.to)
                # 打印发送时间和发送状态：
                print('发送时间：%s \n状态：发送成功！' % send_time) 
                print('短信内容：\n'+message.body) # 打印短信内容
                print('短信SID：' + message.sid) # 打印SID
        return render(request,'monitor-informsuccess.html',locals())

    def monitorcheck(request):
        m_sno=request.session['username']  #得到用户名
        mm_list=student.objects.filter(sno=m_sno) #根据学生表得到该用户名的学生干部
        mm = mm_list[0] #取符合的第一条记录
        if mm:
            m_deptid=mm.sdept_id #得到管理的学院编号
            print("m_dept: ",m_deptid)
            dept = department.objects.filter(id=m_deptid)#找该学院编号对应的学院记录
            print("dept: ",dept)
            mm_dept=dept[0] #取第一条记录
            mm_name=mm_dept.dept_name
            print("mm_name: ",mm_name)
            mm_num=mm_dept.num
            print("mm_num: ",mm_num)
            dorm = dormitory.objects.filter(num=mm_num)  #在宿舍表根据学院楼号得到所有该学院的宿舍
        return render(request,'monitor-check.html',locals())
    """ def editinfoshow(request):
        return render(request,'monitor-edit.html',locals()) """
    def editinfoshow(request):
        dno = request.GET.get('dno')
        num = request.GET.get('num')
        dorm = dormitory.objects.filter(num=num,dno=dno)
        dorm = dorm[0]
        return render(request,'monitor-edit.html',locals())
    def monitoredit(request):
        dno = request.GET.get('dno')
        num = request.GET.get('num')
        print("**dno: ",dno)
        print("**num:",num)
        dorm = dormitory.objects.get(num=num,dno=dno)
        temp=dorm #临时变量存数据
        if request.method=='POST':
            m_year=request.POST.get("year","")
            m_month=request.POST.get("month","")
            m_day=request.POST.get("day","")
            m_content=request.POST.get("content","")
            m_text=request.POST.get("text","")
            if m_year: #有输入
                dorm.year=m_year
            else:
                dorm.year=temp.year

            if m_month: #有输入
                dorm.month=m_month
            else:
                dorm.month=temp.month

            if m_day: #有输入
                dorm.day=m_day
            else:
                dorm.day=temp.day

            if m_content: #有输入
                dorm.content=m_content
            else:
                dorm.content=temp.content

            if m_text: #有输入
                dorm.text=m_text
            else:
                dorm.text=temp.text
            print("年月日，情况，方案：",m_year,m_month,m_day,m_content,m_text)
            dorm.save()
        return render(request,'monitor-edit.html',locals())
