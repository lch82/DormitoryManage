from django.db import models



DEPT = (
    ('计算机科学与技术学院', '计算机科学与技术学院'),
    ('电气与自动化学院', '电气与自动化学院'),
    ('外国语学院', '外国语学院'),
    ('理学院', '理学院'),
) 
#学院表：学院序号（自动生成）、学院名称
class department(models.Model):
    #dept_id = models.CharField('学院序号',max_length=20,primary_key=True)
    dept_name = models.CharField(max_length=100, verbose_name=u"学院名称",choices=DEPT, null=True)
    #dept_name = models.CharField(max_length=100, verbose_name=u"学院名称", null=True)
    #dept_name = models.CharField(max_length=100, verbose_name=u"学院名",choices=DEPT, default="计算机科学与技术学院",null=True)
    num = models.CharField('所在楼号',max_length=2,default=00)
    class Meta:
        db_table = 'department'
        verbose_name = u'学院'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        #return self.dept_id
        return self.dept_name 

""" # Create your models here.
#用户账号表：账号、密码、角色
class Account(models.Model):
    username=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    roles=models.ManyToManyField(to="Role")

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __str__(self): return self.username """
 
#学生表：学号、密码、姓名、寝室号、学院序号、年级、邮箱
class student(models.Model):  
    #dept_id = models.ForeignKey(department, verbose_name=u"学院编号", on_delete=models.CASCADE, null=True)  # 学院序号
    sdept = models.ForeignKey(department, verbose_name=u"学院", on_delete=models.CASCADE, null=True)  # 学院
    #sdept = models.CharField(max_length=100, verbose_name=u"学院名称",choices=DEPT, null=True)
    sclass = models.CharField('年级',max_length=2,default=00) #年级
    sno = models.CharField('学号', max_length=20, primary_key=True)  # 学号
    spass = models.CharField('密码', max_length=40, default='123456')  # 密码
    name = models.CharField('姓名', max_length=20)  # 姓名
    dno = models.CharField('寝室号',max_length=3,default=000) #寝室号
    email = models.EmailField('邮箱', default=None)  # 邮箱
    phone = models.CharField('电话号码', max_length=20,null=True)  # 电话号码
    roles=models.ManyToManyField(to="Role")

    class Meta:  # 表名
        db_table = 'student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):  # 主键
        return self.sno 
#教师表
class teacher(models.Model):  
    sclass = models.CharField('管理年级/管理楼号',max_length=2,default=00) #年级
    tno = models.CharField('用户名', max_length=20, primary_key=True)  # 学号
    spass = models.CharField('密码', max_length=40, default='123456')  # 密码
    roles=models.ManyToManyField(to="Role")

    class Meta:  # 表名
        db_table = 'teacher'
        verbose_name = '教工'
        verbose_name_plural = verbose_name

    def __str__(self):  # 主键
        return self.tno


 #角色表：角色名、权限
class Role(models.Model):
    title=models.CharField(max_length=32)
    permissions=models.ManyToManyField(to="Permission")

    class Meta:
        verbose_name = u'角色'
        verbose_name_plural = verbose_name

    def __str__(self): return self.title
 
 #权限表：权限名、url（一个权限实际上对应一个url）、动作、所属的权限组
class Permission(models.Model):
    title=models.CharField(max_length=32)
    url=models.CharField(max_length=32)
    #action=models.CharField(max_length=32,default="")
    #group=models.ForeignKey("PermissionGroup",default=1,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = u'权限'
        verbose_name_plural = verbose_name
    
    def __str__(self):return self.title
 
 #权限组表：权限组的名字
""" class PermissionGroup(models.Model):
    title = models.CharField(max_length=32)
    
    class Meta:
        verbose_name = u'权限组'
        verbose_name_plural = verbose_name

    def __str__(self): return self.title """

#寝室表:寝室号、寝室人数
class dormitory(models.Model):
    dno = models.CharField('寝室号',max_length=3,primary_key=True)
    num = models.CharField('所在楼号',max_length=2,default=00)
    content = models.CharField('卫生检查情况',max_length=40,default=None) #卫生检查情况（优、良、中、及格、不及格）
    people = models.IntegerField('宿舍人数',default=4)
    sclass = models.CharField('所属年级',max_length=2,default=00) #年级
    text = models.CharField('整改方案',max_length=250,default='无')
    year = models.CharField('年',max_length=6,default='0000')
    month = models.CharField('月',max_length=6,default='00')
    day = models.CharField('日',max_length=6,default='00')
    class Meta:
        db_table = 'dormitory'
        verbose_name = '寝室'
        verbose_name_plural = verbose_name

    def __str__(self):  # 主键
        return self.dno