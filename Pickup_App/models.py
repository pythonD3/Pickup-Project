from django.db import models

# Create your models here.
class User_Detail(models.Model):
	username = models.CharField(max_length = 100,null=True, blank=True)
	password = models.CharField(max_length = 100,null=True, blank=True)
	name = models.CharField(max_length = 100,null=True, blank=True)
	phone_no = models.CharField(max_length = 100,null=True, blank=True)
	zipcode = models.CharField(max_length = 100,null=True, blank=True)
	email_id = models.CharField(max_length = 100,null=True, blank=True)
	token = models.CharField(max_length=2000,null=True,blank=True)
	profile_image = models.ImageField(null = True, blank = True, upload_to = "Profile_Image/")
	
	
	def __str__(self):
		return self.username
	
	class Meta:
		verbose_name="User_Detail"
		verbose_name_plural = "User_Detail"
	
class Child_Detail(models.Model):
	fk_user = models.ForeignKey(User_Detail , on_delete = models.CASCADE , null=True , blank = True)
	name = models.CharField(max_length = 100,null=True,blank=True)
	age = models.CharField(max_length = 100,null=True,blank=True)
	grade = models.CharField(max_length = 50,null=True,blank=True)
	
	class Meta:
		verbose_name="Child_Detail"
		verbose_name_plural = "Child_Detail"
		
class Group_Detail(models.Model):
	fk_user  = models.ForeignKey(User_Detail,on_delete=models.CASCADE,null=True,blank=True)
	group_name    = models.CharField(max_length=100,null=True,blank=True)
	group_member_list = models.TextField(null=True , blank = True)
	created_group_date = models.DateField(null = True, blank = True)
	time =  models.TimeField(null =True, blank = True)
	
	def __str__(self):
		return self.group_name
	

	class Meta:
		verbose_name="Group_Detail"
		verbose_name_plural = "Group_Detail"
		

class Pickup_Schedule_Detail(models.Model):
	fk_user = models.ForeignKey(User_Detail,on_delete=models.CASCADE,null=True,blank=True)
	date =  models.DateField(null = True, blank = True)
	time = models.TimeField(null =True, blank = True)
	request = models.TextField(max_length = 100 , null =True, blank = True)
	schedule_type =  models.CharField(max_length=100,null=True,blank=True)
	fk_child = models.ForeignKey(Child_Detail, on_delete=models.CASCADE, null=True, blank=True)
	flag_status =  models.CharField(max_length=100,null=True,blank=True)
	
	def __str__(self):
		return self.request
	


	class Meta:
		verbose_name="Pickup_Schedule_Detail"
		verbose_name_plural = "Pickup_Schedule_Detail"
		
class Accept_Pickup_Detail(models.Model):
	fk_user = models.ForeignKey(User_Detail,on_delete=models.CASCADE,null=True,blank=True)
	fk_group =  models.ForeignKey(Group_Detail,on_delete=models.CASCADE,null=True,blank=True)
	fk_pick_sched =  models.ForeignKey(Pickup_Schedule_Detail,on_delete=models.CASCADE,null=True,blank=True)
	date =  models.DateField(null = True, blank = True)
	time = models.TimeField(null =True, blank = True)
	fk_child = models.ForeignKey(Child_Detail, on_delete=models.CASCADE, null=True, blank=True)
	request = models.TextField(max_length = 100 , null =True, blank = True)
	
	class Meta:
		verbose_name="Accept_Pickup_Detail"
		verbose_name_plural = "Accept_Pickup_Detail"
		
		

class ChatMaster(models.Model):
	fk_pick_sched =  models.ForeignKey(Pickup_Schedule_Detail,on_delete=models.CASCADE,null=True,blank=True)
	user1_id = models.CharField(max_length = 10,null=True,blank=True)
	user2_id = models.CharField(max_length = 10,null=True,blank=True)
	
	class Meta:
		verbose_name="ChatMaster"
		verbose_name_plural = "ChatMaster"

class ChatChild(models.Model):
	fk_chat_master = models.ForeignKey(ChatMaster,null = True, db_column='fk_chat_master',on_delete=models.CASCADE)
	message = models.TextField(null = True , blank = True)
	date = models.DateField(null = True , blank = True)
	time = models.TimeField(null = True , blank = True)
	user_id = models.CharField(max_length = 10,null=True,blank=True)

	class Meta:
		verbose_name="ChatChild"
		verbose_name_plural = "ChatChild"
	
	
################################### Not in use
	
	
class Chatting_Master(models.Model):	
	fk_user = models.ForeignKey(User_Detail,on_delete=models.CASCADE,null=True,blank=True)
	fk_accept = models.ForeignKey(Accept_Pickup_Detail,on_delete=models.CASCADE,null=True,blank=True)
	fk_pick_sched =  models.ForeignKey(Pickup_Schedule_Detail,on_delete=models.CASCADE,null=True,blank=True)

	class Meta:
		verbose_name = "Chatting_Master"
		verbose_name_plural = "Chatting_Master"
		
class Chatting_Child(models.Model):
	fk_chat_master = models.ForeignKey(Chatting_Master,on_delete=models.CASCADE,null=True,blank=True)
	message = models.TextField(null=True,blank=True)
	date =  models.DateField(null = True, blank = True)
	time = models.TimeField(null =True, blank = True)
	message_from = models.CharField(max_length=100,null=True,blank=True)
	user_id = models.CharField(max_length = 10 , null=True , blank=True)
	
	class Meta:
		verbose_name = "Chatting_Child"
		verbose_name_plural="Chatting_Child"