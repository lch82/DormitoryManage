from django.contrib import admin
from .models import *
#进行后台管理
class PerConfig(admin.ModelAdmin):
    list_display = ["title","url"]
#admin.site.register(Account)
admin.site.register(Role)
admin.site.register(Permission,PerConfig)
admin.site.register(department)
admin.site.register(student)
admin.site.register(teacher)
admin.site.register(dormitory)