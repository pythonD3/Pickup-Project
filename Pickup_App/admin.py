from django.contrib import admin
from .models import *

# Register your models here.



class User_Detail_class(admin.ModelAdmin):
	list_display = ('id', 'username','name','phone_no','zipcode')
admin.site.register(User_Detail , User_Detail_class)


class Child_Detail_class(admin.ModelAdmin):
	list_display = ('id','fk_user','name','age','grade')
admin.site.register(Child_Detail , Child_Detail_class)


class Group_Detail_class(admin.ModelAdmin):
	list_display = ('id','fk_user','group_name','created_group_date')
admin.site.register(Group_Detail , Group_Detail_class)

class Pickup_Schedule_Detail_class(admin.ModelAdmin):
	list_display = ('id','fk_user','schedule_type','request','date')
admin.site.register(Pickup_Schedule_Detail , Pickup_Schedule_Detail_class)


class Accept_Pickup_Detail_class(admin.ModelAdmin):
	list_display = ('id','fk_user','fk_group','fk_pick_sched','date')
admin.site.register(Accept_Pickup_Detail , Accept_Pickup_Detail_class)