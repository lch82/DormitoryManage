#写一个类，最终写到setting.py的MIDDLEWARE
import re
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponse,redirect

""" class ValidPermission(MiddlewareMixin):
    #def process_request(self,request):
    def process_request(self,request):
        # 当前访问路径
        print("TEST7 HERE!!!!!!")
        current_path = request.path_info #获得当前路径
        print("**current_path**")
        print(current_path)

        # 检查是否属于白名单，如果是下面路径url不用校验
        valid_url_list=["/login/","/admin/.*",'/logout/']

        for valid_url in valid_url_list:
            ret=re.match(valid_url,current_path)
            if ret:
                return None
        print("**HERE1**")
        # 校验是否登录，这步是为了让用户去登陆，而不是返回一个没有权限的页面
        user_id=request.session.get("user_id")
        if not user_id:
            return redirect("/login/")

        # 校验url，如果这个url在权限字典的url里，则采取相应的动作，否则提示没有访问权限
        permission_dict=request.session.get("permission_dict")
        print("**HERE2**")
        print(permission_dict)
        for item in permission_dict.values():
            print("1")
            print(item)
            urls=item['urls']
            print("2")
            print(urls)
            for reg in urls:
                reg="^%s$"%reg
                print("3")
                print(reg)
                ret=re.match(reg,current_path)
                print("4")
                print(ret)
                if ret:
                    request.actions=item['actions']
                    print("TEST4 HERE!!!!!")
                    print(request.actions)
                    return None

        return HttpResponse("没有访问权限！") """

class ValidPermission(MiddlewareMixin):
    #def process_request(self,request):
    def process_request(self,request):
        # 当前访问路径
        current_path = request.path_info #获得当前路径
        print("访问url,current_path:  ",current_path)
        # 检查是否属于白名单，如果是下面路径url不用校验
        valid_url_list=["/login/","/admin/.*",'/logout/']

        for valid_url in valid_url_list:
            ret=re.match(valid_url,current_path)
            if ret:
                return None

        # 校验是否登录，这步是为了让用户去登陆，而不是返回一个没有权限的页面
        user_id=request.session.get("user_id")
        if not user_id:
            return redirect("/login/")
        # 校验url，如果这个url在权限字典的url里，则采取相应的动作，否则提示没有访问权限
        flag=False
        permission_dict=request.session.get("permission_dict")
        print("权限url:  ",permission_dict)
        for url in permission_dict:
            """ url_pattern = settings.REGEX_URL.format(url=url)
            print("url_pattern:  ",url_pattern)
            if re.match(url_pattern, current_path):
                flag = True
                break """
            if re.match(url, current_path):
                flag = True
                break
        if flag:
            return None
        else:
            if settings.DEBUG:
                info ='<br/>' + ( '<br/>'.join(permission_dict))
                return HttpResponse('无权限，请尝试访问以下地址：%s' %info)
            else:
                return HttpResponse('无权限访问')   
            """ reg=urls
            reg="^%s$"%reg
            print("3")
            print(reg)
            ret=re.match(reg,current_path)
            print("4")
            print(ret)
            if ret:
                    #request.actions=item['actions']
                    #print("TEST4 HERE!!!!!")
                    #print(request.actions)
                print("OK！")
                return None """

