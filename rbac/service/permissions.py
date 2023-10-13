from rbac import rbac

""" def initial_session(user,request):
    #获取当前用户所在的所有角色拥有的权限url，权限组id，动作，去掉重复
    permissions = user.roles.all().values("permissions__url","permissions__group_id","permissions__action").distinct()
    print("TEST3 HERE!!!!!")
    print(permissions)
    #把结果放到一个字典中
    permission_dict={}
    for item in permissions:
        
        #获取一个组id
        gid=item.get('permissions__group_id')

        #判断当前组id是否已经存在到字典中
        if not gid in permission_dict:
            #如果当前组id不存在，添加当前组id的url和动作
            #加逗号是因为考虑还有数据，举例如下：
            #permission_dict{1:{"url":["/device_list/"],"action":"[search"]},2:{"url":["/device_list/"],"action":["search"}]}
            permission_dict[gid]={
                "urls":[item["permissions__url"],],
                "actions":[item["permissions__action"],]
            }
        else:  #如果当前组id存在，则在当前组id中继续加入url和动作（一个权限组id中有多个权限）
            permission_dict[gid]["urls"].append(item["permissions__url"])
            permission_dict[gid]["actions"].append(item["permissions__action"])

    request.session['permission_dict'] = permission_dict """

def initial_session(user,request):
    #获取当前用户所在的所有角色拥有的权限url，权限组id，动作，去掉重复
    permissions = user.roles.all().values("permissions__url").distinct()
    print("TEST3 HERE!!!!!")
    print(permissions)
    #把结果放到一个字典中
    permission_dict=[]
    for item in permissions:
        
        #获取一个组id
        url=item.get('permissions__url')
        print("***url***:  ",url)
        #判断当前组id是否已经存在到字典中
        if not url in permission_dict:
            permission_dict.append(url)
        

    request.session['permission_dict'] = permission_dict
    print("TEST4 HERE!!!!!")
    print(request.session['permission_dict'])    