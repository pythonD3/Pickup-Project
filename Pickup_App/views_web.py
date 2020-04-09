from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json, string
import traceback
from datetime import date, datetime
from collections import Counter
import ast
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import requests
from Pickup.settings import EMAIL_HOST_USER
from datetime import datetime,date,time
from pyfcm import FCMNotification
import ast
import base64
import random
import math

# #############################Upload image


@csrf_exempt
def upload_image(img, img_path, img_name):
	current = str(datetime.now().strftime('%Y-%m-%d'))
	path = settings.BASE_DIR + "/media/"
	random_number = '{:04}'.format(random.randrange(1, 10**4))
	imgN= img_path+img_name+random_number+"_"+current+'.jpg'
	destination = open(path+imgN, 'wb')
	destination.write(base64.b64decode(img))
	destination.close()
	return imgN



################################Register API

@csrf_exempt
def user_signup_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		username=data['username']
		password = data['password']
		name= data['name']
		phone_no= data['phone_no']
		zipcode= data['zipcode']
		child_list=data['child']
		token=data['token']
		email_id=data['email_id']
		email_id = email_id.lower()
		if User_Detail.objects.filter(username=username).exists():
			send_data = {'msg':"Username already exist",'status':"0"}
			
			
		else:
			obj = User_Detail.objects.create(username=username,password=password,name=name,phone_no=phone_no,
			zipcode=zipcode,email_id=email_id,token=token)
			obj.save()

			for i in child_list:
				print("child", i)
				if i:
					child_obj=Child_Detail(fk_user_id=obj.id, name=i['name'],age=i['age'],grade=i['grade'])
					child_obj.save()
				else:
					pass
			
			send_data = {'msg':"Register successful",'status':"1","user_id": str(obj.id)}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
 #################################################Login Api
 
@csrf_exempt
def user_login_web(request):
	try:
		data= json.loads(request.body.decode('utf-8'))
		username = data['username']
		password = data['password']
		
		# if User_Detail.objects.filter(username=username).exists():
		if User_Detail.objects.filter(username=username,	password = password).exists():
			obj = User_Detail.objects.get(username=username, password = password)
			
			send_data = {'msg' : "Login Sucessfully", 'status':"1", "user_id": str(obj.id)}
		else:
			send_data = {'msg':"Invalid Credentials", 'status':"0"}
		# else:
			# send_data = {'msg':"Username is incorrect", 'status':"0"}
		
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
################################Forget password

	
@csrf_exempt
def forget_password_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		email_id = data['email_id']
		email_id = email_id.lower()
		print("email_id----->",email_id)
		if User_Detail.objects.filter(email_id = email_id).exists():
			obj = User_Detail.objects.get(email_id = email_id)
			cust_email = obj.email_id
			print("cust_email",cust_email)
			rstr = "\n\nThanks,"+"\nPickup Team"
			# new=rstr.rjust(100)
			subject = "Request For Password Recovery";
			# message = "Hi "+obj.name+", \nYou have recently requested password for Pickup user account.\n\nYour current password is "+obj.password+"\n\nIf you did not request a password, please ignore this email or reply to let us know.\n\nThanks,\Pickup Team"
			message = "Hi "+obj.name+", \nYou have recently requested password for Pickup user account.\n\nYour current password is "+obj.password+"\n\nIf you did not request a password, please ignore this email or reply to let us know."+rstr
			print("message---------->",message)
			from_mail = settings.EMAIL_HOST_USER
			
			print("from_mail------->",from_mail)
			email_msg =EmailMessage(subject, message, to=[email_id], from_email= from_mail )
			
			print("email_msg   ---------->",email_msg)
			
			email_msg.send()
			print("message..........*",email_msg)
			send_data = {'msg' : "Password has been sent to your registered email id" , 'status': "1"}
		else:
			send_data = {'msg':"Email Does not Exist", 'status':"0"}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	

	########################################### Change Password 
@csrf_exempt
def user_change_password_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		current_password = data['current_password']
		new_password = data['new_password']
		
		if User_Detail.objects.filter(id = user_id).exists():
			obj = User_Detail.objects.get(id = user_id)
			if obj.password == current_password:
			
				current_password = new_password
				obj.password = current_password
				obj.save()
				send_data = {'msg':"Password Changed Sucessfully", 'status':"1"}
			else:
				send_data = {'msg':"Incorrect Password","status":"0"}
		else:
			send_data = {'msg' :"User Not Found", 'status':"0"}
		
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
################################################### all user list api 
@csrf_exempt
def user_list_web(request):
	try:
		data= json.loads(request.body.decode('utf-8'))
		user_id=data['user_id']
		list = []
		dict={}
		if User_Detail.objects.filter(id=user_id).exists():
			obj = User_Detail.objects.all().exclude(id=user_id)
			for i in obj:
				if i.id:
					dict['user_id'] = str(i.id)
				else:
					dict['user_id'] = ""
				if i.username:
					dict['username'] = str(i.username)
				else:
					dict['username'] = ""
				if i.name:
					dict['name'] = str(i.name)
				else:
					dict['name'] = ""
				if i.zipcode:
					dict['zipcode'] = str(i.zipcode)
				else:
					dict['zipcode'] = ""
					
				if i.phone_no:
					dict['phone_no'] = str(i.phone_no)
				else:
					dict['phone_no'] = ""
				
				child_count = Child_Detail.objects.filter(fk_user_id=i.id)
				count = child_count.count()
				print ("child_count",child_count)
				print ("count",count)
				dict['child_count'] = str(count)
				list.append(dict)
				dict={}
				
				
			send_data = {'msg':"User List", 'status':"1",'list':list}
		else:
			send_data = {'msg':"User List Empty", 'status':"0"}

	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	# #####################################################User update with id
	
@csrf_exempt
def update_user_profile_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		name= data['name']
		phone_no= data['phone_no']
		zipcode= data['zipcode']
		child_list=data['child']
		profile_image=data['profile_image']
		email_id=data['email_id']
		email_id = email_id.lower()
		
		if User_Detail.objects.filter(id=user_id).exists():
			obj= User_Detail.objects.get(id=user_id)
			obj.name = name
			obj.phone_no = phone_no
			obj.zipcode = zipcode
			obj.email_id = email_id
			if profile_image:
				profile_image_name= upload_image(profile_image, "Profile_Image/", "Profile_Image_")
				obj.profile_image=profile_image_name
			else:
				pass
			obj.save()
			for i in child_list:
				print("chld", i)
				if len(i)>0:
					print("le",len(i))
					child_obj=Child_Detail.objects.get(id=user_id)
					child_obj.name =i['name']
					child_obj.age = i['age']
					child_obj.grade = i['grade']
					child_obj.save()
				else:
					pass
				send_data = {'msg':"User Profile Updated",'status':"1"}
		else:
			
			send_data = {'msg':"User Not Found",'status':"0"}
		
		
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
	
	
	# ###################################################user list according to ID 
	
@csrf_exempt
def user_list_by_id_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		
		if User_Detail.objects.filter(id=user_id).exists():
			i= User_Detail.objects.get(id=user_id)
			# list = []
			dict ={}
			if i.id:
				dict['user_id'] = str(i.id)
			else:
				dict['user_id'] = ""
			if i.username:
				dict['username'] = str(i.username)
			else:
				dict['username'] = ""
			if i.name:
				dict['name'] = str(i.name)
			else:
				dict['name'] = ""
			if i.zipcode:
				dict['zipcode'] = str(i.zipcode)
			else:
				dict['zipcode'] = ""
				
			if i.phone_no:
				dict['phone_no'] = str(i.phone_no)
			else:
				dict['phone_no'] = ""
					
			if i.email_id:
				dict['email_id'] = str(i.email_id)
			else:
				dict['email_id'] = ""	

			if i.profile_image:
				dict['profile_image'] = str(i.profile_image)
			else:
				dict['profile_image'] = ""
			
			# list.append(dict)
			# dict={}
			
			
			child_obj = Child_Detail.objects.filter(fk_user_id=i.id)
			
			chlid_list = []
			child_dict={}
			for j in child_obj:
				if j.id:
					child_dict['child_id'] = str(j.id)
				else:
					child_dict['child_id'] = ""
				if j.name:
					child_dict['name'] = str(j.name)
				else:
					child_dict['name'] = ""
				if j.age:
					child_dict['age'] = str(j.age)
				else:
					child_dict['age'] = ""
				if j.grade:
					child_dict['grade'] = str(j.grade)
				else:
					child_dict['grade']=""
					
				chlid_list.append(child_dict)
				child_dict={}
				
				
			send_data = {'msg':"User list  by id",'status':"1",'user_list':dict,"chlid_list":chlid_list}
		else:
			send_data = {'msg':"User Not Found",'status':"0"}
		
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)

	############################ Change password 
	
	

@csrf_exempt
def change_password(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		new_password = data['new_password']
		old_password = data['old_password']
		
		if User_Detail.objects.filter(id = user_id).exists():
			obj = User_Detail.objects.get(id = user_id)
			
			if obj.password == old_password:
				obj.password = new_password
				obj.save()
				send_data = {'msg':"Password changed successfully","status":"1"}
				
			else:
				send_data = {'msg':"Incorrect old password","status":"0"}
		else: 
			send_data = {'msg':"User is not registered", 'status':"0"}
			
	except:
		send_data = {'msg':'Something went wrong, please try after sometime.','status':"0","error":str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)

	
	
################################################ Create Group Api

@csrf_exempt
def create_group_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		group_name = data['group_name']
		group_member_list = data['group_member']
		date = data['date']
		time = data['time']
		
		
		print("group_member_list...............",group_member_list)
	
	
		if time== "":
			now=datetime.now()
			order_time = now.strftime('%H:%M:%S')
			time_now = order_time
		else:
			time_now = time	
				
		if date== "":
			current_date = datetime.now().date()
		else:
			current_date = date
			
		# current_date = datetime.now().date()
		# now=datetime.now()
		# order_time = now.strftime('%H:%M:%S')
		# time_now = order_time
		# print("current_date",current_date)
		if User_Detail.objects.filter(id=user_id).exists():
			group_obj = Group_Detail(fk_user_id=user_id,group_name=group_name,group_member_list=json.dumps(group_member_list),created_group_date=current_date,time=time_now)
			group_obj.save()
			send_data = {'msg':"Group created successfully",'status':"1",'group_id':str(group_obj.id)}
		else:
			send_data = {'msg':"User Not Found",'status':"0"}
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
################################################Group list

@csrf_exempt
def group_list_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		print("user id ",user_id)
		if	User_Detail.objects.filter(id = user_id).exists():
			all_group_obj = Group_Detail.objects.all().exclude(fk_user__id = user_id)
			group_obj = Group_Detail.objects.filter(fk_user__id = user_id)
			print("group_obj----",group_obj)
			list = []
			dict = {}
			
			for i in group_obj:		
				dict['group_id'] = str(i.id) if i.id else ""
				dict['group_name'] = str(i.group_name) if i.group_name else ""
				dict['member_type'] = "Admin"
				if i.group_member_list:
					# print(i.group_member_list)
					# gr_count = i.group_member_list
					# print("type",type(i.group_member_list))
					# new_list = ast.literal_eval(gr_count)
					# print("new list ", new_list)
					# lenth_l=len(new_list)
					# print("length of gr_count",lenth_l)
							
					dict['group_member_count'] = str(len(json.loads(i.group_member_list)))
				else:
					dict['group_member_count'] = "0"
				
				list.append(dict)
				dict={}
			
			for j in all_group_obj:
				if user_id in json.loads(j.group_member_list):
					dict['group_id'] = str(j.id) if j.id else ""
					dict['group_name'] = str(j.group_name) if j.group_name else ""
					dict['member_type'] = "Normal"
					if j.group_member_list:
						# print(i.group_member_list)
						# gr_count = i.group_member_list
						# print("type",type(i.group_member_list))
						# new_list = ast.literal_eval(gr_count)
						# print("new list ", new_list)
						# lenth_l=len(new_list)
						# print("length of gr_count",lenth_l)
								
						dict['group_member_count'] = str(len(json.loads(j.group_member_list)))
					else:
						dict['group_member_count'] = "0"
					
					list.append(dict)
					dict={}
				else:
					pass
			send_data ={'msg':"Group member list",'status':"1",'member_list':list}
		else:
			send_data ={'msg':"User Not Found",'status':"0"}

	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)

######################################### Save schedule data api

	
@csrf_exempt
def save_schedule_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']	
		schedule_type=data['schedule_type']
		date = data['date']
		time = data['time']
		request = data['data']
		child_name = data['child_name']
		print("time",time)
		print("child_name",child_name)
		
		if User_Detail.objects.filter(id=user_id).exists():
			print("user_id",user_id)
			if child_name:
				print("Pickup")
				if Child_Detail.objects.filter(fk_user_id=user_id, name=child_name).exists():
				
					if schedule_type == "Pickup":
						type = "Pickup"
						flag_status = "0"
					else:
						type = "Help"
						flag_status ="0"
						
					if time== "":
						now=datetime.now()
						order_time = now.strftime('%H:%M:%S')
						time_now = order_time
					else:
						time_now = time	
						
					if date== "":
						date_n = datetime.now().date()
					else:
						date_n = date
						
					sched_obj=Pickup_Schedule_Detail(fk_user_id = user_id, schedule_type=type,date=date_n,time=time_now,request=request,fk_child =Child_Detail.objects.get(name=child_name), flag_status=flag_status)
					sched_obj.save()
					
					
					##################################  NOTIFICATION CODE	FOR  PICKUP
				
					print(datetime.strptime(str(date_n), "%Y-%m-%d").strftime('%d/%m/%Y'))
					curr_datetime_obj = datetime.strptime(str(date_n), "%Y-%m-%d").strftime('%d/%m/%Y')
					schedule_user=User_Detail.objects.get(id=user_id)
					schedule_user_name = schedule_user.name
					print("schedule_user_name",schedule_user_name)
					
					gr_obj =Group_Detail.objects.filter(fk_user_id = user_id)
					print("gr_obj",gr_obj)
					for j in gr_obj:
						if j.group_member_list:
							new_list = json.loads(json.dumps(j.group_member_list))
							new_list = ast.literal_eval(new_list) 
							print('new_list,',new_list)
							for user in new_list:
								print("user id",user)
								user=User_Detail.objects.get(id=user)
								device_token = user.token
								api_key = settings.API_KEY_NOTIFICATION
								push_service = FCMNotification(api_key=api_key)
								message_title = "You got a new pickup request on "+str(j.group_name)
								message_body = str(schedule_user_name)+" has added pickup request on " +curr_datetime_obj
								color = "#ffa000"
								###### data_message = {
								#######		# "title" : "New Help Request",
								########		# "body" : message_body,    	
								###########	# }
								push_service.notify_single_device(registration_id=device_token, message_title=message_title, message_body=message_body,color=color,sound="Default")
								print("date_n",date_n)
					send_data ={'msg':"Schedule save successfully",'status':"1"}
				else:
					send_data ={'msg':"Child Not Found",'status':"0"}
			else:
				if schedule_type == "Pickup":
					type = "Pickup"
					flag_status = "0"
				else:
					type = "Help"
					flag_status ="0"
						
				if time== "":
					now=datetime.now()
					order_time = now.strftime('%H:%M:%S')
					time_now = order_time
				else:
					time_now = time	
						
				if date== "":
					date_n = datetime.now().date()
				else:
					date_n = date
						
				sched_obj=Pickup_Schedule_Detail(fk_user_id = user_id, schedule_type=type,date=date_n,time=time_now,request=request, flag_status=flag_status)
				sched_obj.save()
				##################################  NOTIFICATION CODE	FOR  HELP
			
				print(datetime.strptime(str(date_n), "%Y-%m-%d").strftime('%d/%m/%Y'))
				curr_datetime_obj = datetime.strptime(str(date_n), "%Y-%m-%d").strftime('%d/%m/%Y')
				schedule_user=User_Detail.objects.get(id=user_id)
				schedule_user_name = schedule_user.name
				print("schedule_user_name",schedule_user_name)
				gr_obj =Group_Detail.objects.filter(fk_user_id = user_id)
				print("gr_obj",gr_obj)
				for j in gr_obj:
					if j.group_member_list:
						new_list = json.loads(json.dumps(j.group_member_list))
						new_list = ast.literal_eval(new_list) 
						print('new_list,',new_list)
						for user in new_list:
							print("user id",user)
							user=User_Detail.objects.get(id=user)
							device_token = user.token
							api_key = settings.API_KEY_NOTIFICATION
							push_service = FCMNotification(api_key=api_key)
							message_title = "You got a new help request  on "+str(j.group_name)
							message_body = str(schedule_user_name)+" has added help request on " +curr_datetime_obj
							color = "#ffa000"
							
						push_service.notify_single_device(registration_id=device_token, message_title=message_title, message_body=message_body,color=color,sound="Default")
							
				send_data ={'msg':"Schedule save successfully",'status':"1"}
		else:
			send_data ={'msg':"User Not Found",'status':"0"}
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
# #################################get schudule api

@csrf_exempt
def get_schedule_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']	
		print("user_id",user_id)
		# if Pickup_Schedule_Detail.objects.filter(fk_user__id=user_id).exists():
		
		obj = Pickup_Schedule_Detail.objects.filter(fk_user__id = user_id).order_by('-date')
		print("object",obj)
		list = []
		dict = {}
		for i in obj:
			if i.id:
				dict['schedule_id'] = str(i.id)
			else:
				dict['schedule_id'] = ""
				
			if i.fk_user:
				dict['username'] = str(i.fk_user.name)
			else:
				dict['username'] = ""
				
			if i.date:
				print("date-------->",i.date)
				print(datetime.strptime(str(i.date), "%Y-%m-%d").strftime('%d/%m/%Y'))
				datetime_obj = datetime.strptime(str(i.date), "%Y-%m-%d").strftime('%d/%m/%Y')
				dict['date'] = datetime_obj
			else:
				dict['date'] = ""
			
			if i.time:
				time_s = i.time
				time_n = time_s.strftime("%I:%M %p")
				dict['time'] = time_n
			else:
				dict['time'] = ""
			if i.schedule_type:
				dict['schedule_type'] = str(i.schedule_type)
			else:
				dict['schedule_type'] = ""
			
			if i.request:
				dict['data'] = str(i.request)
			else:
				dict['data'] = ""
				
			if i.fk_child:
				dict['child_name'] = str(i.fk_child.name)
			else:
				dict['child_name'] = ""
				
			if Accept_Pickup_Detail.objects.filter(id= i.id).exists:
				acc_obj= Accept_Pickup_Detail.objects.filter(fk_pick_sched_id=i.id)
				count = len(acc_obj)
				print("acc_obj",count)
				
				dict['accepted_count'] =  str(count)
			else:
				dict['accepted_count'] =""
				
			list.append(dict)
			dict ={}
			
		if Accept_Pickup_Detail.objects.filter(fk_user__id= user_id).exists:
			acc_object =Accept_Pickup_Detail.objects.filter(fk_user__id= user_id)
			print("acc_object",acc_object)
			count = len(acc_object)
			print("acc_object",count)
			dict_1 = {}
			for j in acc_object:
				if j.fk_pick_sched:
					dict_1['schedule_username'] = str(j.fk_pick_sched.fk_user.name)
				else:
					dict_1['schedule_username'] = ""
					
				if j.fk_pick_sched.id:
					dict_1['schedule_id'] = str(j.fk_pick_sched.id)
				else:
					dict_1['schedule_id'] = ""
					
				if j.date:
					print(datetime.strptime(str(j.date), "%Y-%m-%d").strftime('%d/%m/%Y'))
					datetime_obj = datetime.strptime(str(j.date), "%Y-%m-%d").strftime('%d/%m/%Y')
					dict_1['date'] = datetime_obj
				else:
					dict_1['date'] = ""
				
				if j.time:
					time_s = j.time
					time_n = time_s.strftime("%I:%M %p")
					dict_1['time'] = time_n
				else:
					dict_1['time'] = ""
					
				if j.fk_pick_sched.fk_child:
					dict_1['child_name'] = str(j.fk_pick_sched.fk_child.name)
				else:
					dict_1['child_name'] = ""
								
				if j.fk_pick_sched.schedule_type:
					if  j.fk_pick_sched.schedule_type =="Help":
						dict_1['schedule_type'] = "Pickup"
					else:
						dict_1['schedule_type'] = "Help"
				
				else:
					dict_1['schedule_type'] = ""
					
				if j.fk_pick_sched.request:
					dict_1['data'] = str( j.fk_pick_sched.request)
				else:
					dict_1['data']=  ""
					
				list.append(dict_1)
				dict_1 = {}			
				# else:
					# send_data ={'msg':"Schedule Not Found",'status':"0"}
				
			send_data ={'msg':"Schedule list",'status':"1",'schedule_list':list}
		# else:
			# send_data ={'msg':"User Not Found",'status':"0"}
		
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	# ########################Dlete Schedule Api
	

@csrf_exempt
def delete_schedule_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']	
		schedule_id = data['schedule_id']	
		if Pickup_Schedule_Detail.objects.filter(fk_user_id=user_id).exists():
			sched_obj = Pickup_Schedule_Detail.objects.get(fk_user_id=user_id,id= schedule_id)
			sched_obj.delete()
			send_data ={'msg':"Schedule deleted ",'status':"1"}
		else:
			send_data ={'msg':"User Not Found",'status':"0"}
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	
################ Schedule List for Group
	
@csrf_exempt
def schedule_list_for_gruop_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']	
		group_id = data['group_id']	
		
		print("group_id",group_id)
		if User_Detail.objects.filter(id=user_id).exists():
			if	Group_Detail.objects.filter(id=group_id).exists():
				gr_obj = Group_Detail.objects.get(id=group_id)
				gr_list = json.loads(gr_obj.group_member_list)
				print("llllll",gr_list)
				gr_list.append(str(gr_obj.fk_user.id))
				print("list...",gr_list)
				gr_list.remove(str(user_id))
				print("nw list....", gr_list)
				
				gr_date = datetime.strptime(str(gr_obj.created_group_date), "%Y-%m-%d").strftime('%d/%m/%Y')
				gr_time = gr_obj.time.strftime("%I:%M %p")
				print("gr_date",gr_date)
				print("gr_time",gr_time)
				
				obj = Pickup_Schedule_Detail.objects.filter(fk_user__id__in = gr_list).order_by('-date')
				list = []
				dict = {}
				for i in obj:
					print(i.fk_user.id)
					##########Time  comparison for not getting old schedule code in new group
					pick_date=datetime.strptime(str(i.date), "%Y-%m-%d").strftime('%d/%m/%Y')
					pick_time = i.time.strftime("%I:%M %p")
					print("pick_date",pick_date)
					print("pick_time",pick_time)
					
					if gr_date>pick_date:
						print("hello")
						send_data ={'msg':"Schedule Not Found",'status':"0"}
					else:
					
						if i.id:
							dict['schedule_id'] = str(i.id)
						else:
							dict['schedule_id'] = ""
							
						if i.fk_user:
							dict['username'] = str(i.fk_user.name)
						else:
							dict['username'] = ""
							
						if i.date:
							#### print("date-------->",i.date)
							##### print(datetime.strptime(str(i.date), "%Y-%m-%d").strftime('%d/%m/%Y'))
							datetime_obj = datetime.strptime(str(i.date), "%Y-%m-%d").strftime('%d/%m/%Y')
							dict['date'] = datetime_obj
						else:
							dict['date'] = ""
						
						if i.time:
							time_s = i.time
							time_n = time_s.strftime("%I:%M %p")
							dict['time'] = time_n
						else:
							dict['time'] = ""
							
						if i.schedule_type:
							dict['schedule_type'] = str(i.schedule_type)
						else:
							dict['schedule_type'] = ""
						
						if i.request:
							dict['data'] = str(i.request)
						else:
							dict['data'] = ""
							
						if i.fk_child:
							dict['child_name'] = str(i.fk_child.name)
						else:
							dict['child_name'] = ""
							
						if Accept_Pickup_Detail.objects.filter(fk_user_id=user_id,fk_group_id=group_id,fk_pick_sched_id=i.id).exists():
							acc_obj = Accept_Pickup_Detail.objects.filter(fk_user_id=user_id,fk_group_id=group_id,fk_pick_sched_id=i.id)
							dict['flag_status'] = "Accepted"
						else:
							dict['flag_status'] = "Pending"
							
						list.append(dict)
						dict ={}
					
					send_data ={'msg':"Schedule list",'status':"1",'schedule_list':list}
				
			else:
				send_data ={'msg':"Group Not Found",'status':"0"}
		else:
			send_data ={'msg':"User Not Found",'status':"0"}
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	
	
################################################ Save help acceptr data

@csrf_exempt
def accept_schedule_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']	
		group_id = data['group_id']	
		schedule_id = data['schedule_id']	
		date = data['date']	
		time = data['time']	
		
		
		if time== "":
			now=datetime.now()
			order_time = now.strftime('%H:%M:%S')
			time_now = order_time
		else:
			time_now = time	
				
		if date== "":
			current_date = datetime.now().date()
		else:
			current_date = date
					
					
		print("schedule_id",schedule_id)
	
		if User_Detail.objects.filter(id=user_id).exists():
			if Group_Detail.objects.filter(id=group_id).exists():
			
				accept_obj = Accept_Pickup_Detail(fk_user_id=user_id, fk_group_id=group_id,fk_pick_sched_id=schedule_id,date=current_date,time=time_now)
				print("accept_obj",accept_obj)
				
				accept_obj.save()
				
				
				# Notification for accept
				# print(datetime.strptime(str(current_date), "%Y-%m-%d").strftime('%d/%m/%Y'))
				curr_datetime_obj = datetime.strptime(str(current_date), "%Y-%m-%d").strftime('%d/%m/%Y')
				pickup_obj=Pickup_Schedule_Detail.objects.get(id=schedule_id)
				pickup_id = pickup_obj.fk_user.id
				print("pickup_id",pickup_id)
				pickup_token =pickup_obj.fk_user.token
				print("pickup_token",pickup_token)
				accept_sched = Accept_Pickup_Detail.objects.filter(fk_pick_sched = schedule_id,fk_user_id=user_id, fk_group_id=group_id)
				for a in accept_sched:
					pickup_sched_id = a.fk_user.id
					pickup_sched_name = a.fk_user.name
					print("pickup_sched_id",pickup_sched_id)
					print("pickup_sched_name",pickup_sched_name)
					
					user=User_Detail.objects.get(id=pickup_id)
					device_token = user.token
					print("device_token",device_token)
					api_key = settings.API_KEY_NOTIFICATION
					push_service = FCMNotification(api_key=api_key)
					message_title = "You got a offer for help request"
					message_body = str(a.fk_user.name) +" accepts your help request for " + curr_datetime_obj
					color = "#ffa000"
					# data_message = {
										# "title" : "New Help Request",
										# "body" : message_body,    	
									# }
					push_service.notify_single_device(registration_id=pickup_token, message_title=message_title, message_body=message_body,color=color,sound="Default")
				
				send_data ={'msg':"Schedule Accepted",'status':"1"}
			
			else:
				send_data ={'msg':"Group Not Found",'status':"0"}
		else:
			send_data ={'msg':"User Not Found",'status':"0"}
		
	
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	
##################################################### accept scedule list api
	
@csrf_exempt
def accept_schedule_list_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']	
		schedule_id = data['schedule_id']	
		
		if	User_Detail.objects.filter(id=user_id).exists():
			if Pickup_Schedule_Detail.objects.filter(id=schedule_id).exists():
			
				obj = Accept_Pickup_Detail.objects.filter(fk_pick_sched_id=schedule_id)
				list=[]
				dict={}
				print("objecttttttttt",obj)
				for i in obj:
				
				
					if i.fk_user.name:
						dict['username'] = str(i.fk_user.name)
					else:
						dict['username'] = ""	
						
					if i.fk_user.phone_no:
						dict['phone_no'] = str(i.fk_user.phone_no)
					else:
						dict['phone_no'] = ""	
						
					if i.fk_pick_sched.request:
						dict['data'] = str(i.fk_pick_sched.request)
					else:
						dict['data'] = ""	
					
					if i.fk_pick_sched.schedule_type:
						dict['schedule_type'] = str(i.fk_pick_sched.schedule_type)
					else:
						dict['schedule_type'] = ""	
						
					if i.date:
						print("date-------->",i.date)
						print(datetime.strptime(str(i.date), "%Y-%m-%d").strftime('%d/%m/%Y'))
						datetime_obj = datetime.strptime(str(i.date), "%Y-%m-%d").strftime('%d/%m/%Y')
						dict['date'] = datetime_obj
					else:
						dict['date'] = ""
					
					if i.time:
						time_s = i.time
						time_n = time_s.strftime("%I:%M %p")
						dict['time'] = time_n
					else:
						dict['time'] = ""
						
						
					if i.request:
						dict['note'] = str(i.request)
					else:
						dict['note'] = ""		
						
					if i.fk_child:
						dict['child_name'] = str(i.fk_child.name)
					else:
						dict['child_name'] = ""	
				
						
					list.append(dict)
					dict ={}
			
				send_data ={'msg':"Accept schedule list",'status':"1","list":list}
			else:
				send_data ={'msg':"User Not Found",'status':"0"}
		else:
			send_data ={'msg':"Accepted List Not Found",'status':"0"}
	
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	
	
	
#####################Save Pickup information
@csrf_exempt
def save_pickup_info_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']	
		schedule_id = data['schedule_id']	
		group_id = data['group_id']	
		date = data['date']	
		time = data['time']	
		request = data['note']	
		child_name = data['child_name']	
	
		print("schedule_id",schedule_id)
	
		if User_Detail.objects.filter(id=user_id).exists():
			if Group_Detail.objects.filter(id=group_id).exists():
				if Child_Detail.objects.filter(fk_user_id=user_id, name=child_name).exists():
			
					if time =="":
						time_now=datetime.now()
					else:
						time_now = time
						
					if date =="":
						current_date=current_date = datetime.now().date()	
					else:
						current_date = date
						
					accept_obj = Accept_Pickup_Detail(fk_user_id=user_id, fk_group_id=group_id,fk_pick_sched_id=schedule_id,date=current_date,time=time_now,fk_child =Child_Detail.objects.get(name=child_name), request=request)
					print("accept_obj",accept_obj)
					
					if Pickup_Schedule_Detail.objects.filter(id=schedule_id,flag_status="0").exists():
						pic_obj = Pickup_Schedule_Detail.objects.get(id=schedule_id,flag_status="0")
						pic_obj.flag_status="1"
						pic_obj.save()
					else:
						send_data={'msg':" exists",'status':"0"}
					accept_obj.save()
					
					########################## Notification code for pickup
				
				# print(datetime.strptime(str(current_date), "%Y-%m-%d").strftime('%d/%m/%Y'))
					curr_datetime_obj = datetime.strptime(str(date), "%Y-%m-%d").strftime('%d/%m/%Y')
					pickup_obj=Pickup_Schedule_Detail.objects.get(id=schedule_id)
					pickup_id = pickup_obj.fk_user.id
					print("pickup_id",pickup_id)
					pickup_token =pickup_obj.fk_user.token
					print("pickup_token",pickup_token)
					accept_sched = Accept_Pickup_Detail.objects.filter(fk_pick_sched = schedule_id,fk_user_id=user_id, fk_group_id=group_id)
					for a in accept_sched:
						pickup_sched_id = a.fk_user.id
						pickup_sched_name = a.fk_user.name
						print("pickup_sched_id",pickup_sched_id)
						print("pickup_sched_name",pickup_sched_name)
						
						user=User_Detail.objects.get(id=pickup_id)
						device_token = user.token
						print("device_token",device_token)
						api_key = settings.API_KEY_NOTIFICATION
						push_service = FCMNotification(api_key=api_key)
						message_title = "You got a offer for pickup request"
						message_body = str(a.fk_user.name) +" accepts your pickup request for " + curr_datetime_obj
						color = "#ffa000"
						# data_message = {
											# "title" : "New Help Request",
											# "body" : message_body,    	
										# }
						push_service.notify_single_device(registration_id=pickup_token, message_title=message_title, message_body=message_body,color=color,sound="Default")
					
					send_data ={'msg':"Information Added Sucessfully",'status':"1"}
				else:
					send_data ={'msg':"Child Not Found",'status':"0"}
			else:
				send_data ={'msg':"Group Not Found",'status':"0"}
		else:
			send_data ={'msg':"User Not Found",'status':"0"}
		
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	
	
	########################################### Group list member api 
	
@csrf_exempt
def group_member_list_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		group_id = data['group_id']
		print("user id ",user_id)
		list = []
		dict={}
		if	User_Detail.objects.filter(id = user_id).exists():
			if Group_Detail.objects.filter(id=group_id).exists():
				j=Group_Detail.objects.get(id=group_id)
				if  j.fk_user.name:
						dict['username'] = str(j.fk_user.name)  	
				else:
					dict['username'] =""
				
				if j.id:
					dict['group_id'] = str(j.id)
				else:
					dict['group_id'] = ""
					
				if j.group_name:
					dict['group_name'] = str(j.group_name)
				else:
					dict['group_name'] = ""
							
			
				if j.group_member_list:
					new_list = json.loads(json.dumps(j.group_member_list))
					new_list = ast.literal_eval(new_list) 
					print('new_list,',new_list)
					member_list=[]
					dict_1={}
					for user in new_list:
						print("user id",user)
						user=User_Detail.objects.filter(id=user)
						
						for m in user:
							if m.name:
								dict_1['name'] = str(m.name)
							else:
								dict_1['name'] =""
							if m.username:
								dict_1['username'] = str(m.username)
							else:
								dict_1['username'] = ""
							if m.id:
								dict_1['user_id'] =str(m.id)
							else:
								dict_1['user_id'] =""
							member_list.append(dict_1)
							dict_1={}
							
							
							print("member_list",member_list)
					dict['group_member_list'] =member_list
				else:
					dict['group_member_list'] =""
					
				list.append(dict)
				dict={}
	
				send_data ={'msg':"Group member list",'status':"1",'member_list':list}
			else:
				send_data ={'msg':"Group Not Found",'status':"0"}
		else:
			send_data ={'msg':"User Not Found",'status':"0"}
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	
	
	
	
	
	
	############################## Save Chatting 
	
@csrf_exempt
def save_chatting_message_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		accept_user_id = data['accept_user_id']
		schedule_id = data['schedule_id']
		message_from = data['message_from']
		message = data['message']
		current_date = data['current_date']
		current_time = data['current_time']
		data_message = {}
		
		if Accept_Pickup_Detail.objects.filter(id = accept_user_id).exists():
			accept_obj = Accept_Pickup_Detail.objects.get(id = accept_user_id)
			sched_obj = Pickup_Schedule_Detail.objects.get(id=schedule_id)
			user_obj = User_Detail.objects.get(id = user_id)
			data_message['accept_id'] = accept_user_id
			data_message['user_id'] = user_id
			data_message['title'] = "New Message"
			data_message['body'] = message
			data_message['notification_type'] = "chat"
			
			
			# if sched_obj.request:
				# data_message['request'] = sched_obj = request
			# else:
				# data_message['request']  = ""
			if user_obj.name:
				data_message['user_name'] = user_obj.name
			else:
				data_message['user_name'] = ""
			if user_obj.phone_no:
				data_message['phone_no'] = user_obj.phone_no
			else:
				data_message['phone_no'] = ""
		
			if accept_obj.fk_user.name:
				data_message['accepted_user_name'] = accept_obj.fk_user.name
			else:
				data_message['accepted_user_name'] = ""
			if accept_obj.fk_user.phone_no:
				data_message['accepted_user_phone_no'] = accept_obj.fk_user.phone_no
			else:
				data_message['accepted_user_phone_no'] = ""
			
			
			print("data_message-----",data_message)
			if Chatting_Master.objects.filter(fk_user__id = user_id,fk_accept__id =accept_user_id).exists():
				chat_master_obj = Chatting_Master.objects.get(fk_user__id = user_id,fk_accept__id =accept_user_id,fk_pick_sched=schedule_id)
				if message_from=="User":	
					chat_child_obj = Chatting_Child(fk_chat_master = chat_master_obj,message=message,date=current_date,time=current_time, message_from = message_from, user_id = accept_user_id)
					chat_child_obj.save()
					
					if accept_obj.fk_user.token:
						res = send_chatting_notification(accept_obj.fk_user.token ,"New Message", message, data_message)
						print(res)
					else:
						pass
						
				elif message_from == "Accepted_User":
					chat_child_obj = Chatting_Child(fk_chat_master = chat_master_obj,message=message,date=current_date,time=current_time, message_from = message_from, user_id = user_id)
					chat_child_obj.save()
					
					if user_obj.token:
						res = send_chatting_notification(user_obj.token, "New Message", message, data_message)
						print(res)
					else:
						pass
				else:
					pass
			else:
				chat_master_obj = Chatting_Master(fk_pick_sched= Pickup_Schedule_Detail.objects.get(id=schedule_id), fk_user = User_Detail.objects.get(id=user_id),fk_accept=Accept_Pickup_Detail.objects.get(id =accept_user_id))
				chat_master_obj.save()
				
				if message_from == "User":
					chat_child_obj = Chatting_Child(fk_chat_master = chat_master_obj,message=message,date=current_date,time=current_time, message_from = message_from, user_id = accept_user_id)
					chat_child_obj.save()
					
					if accept_obj.fk_user.token:
						res = send_chatting_notification(accept_obj.fk_user.token, "New Message", message, data_message)
						print(res)
					else:
						pass
						
				elif message_from == "Accepted_User":
					chat_child_obj = Chatting_Child(fk_chat_master = chat_master_obj,message=message,date=current_date,time=current_time, message_from = message_from, user_id = user_id)
					chat_child_obj.save()
					
					if user_obj.token:
						res = send_chatting_notification(user_obj.token ,"New Message", message, data_message)
						print(res)
					else:
						pass
				else:
					pass
			
			send_data = {'msg':"Message Saved Successfully",'status':"1"}
		else:
			send_data = {'msg':"Accepted Schedule Not Found",'status':"0"}
	except:
		send_data = {'msg':"Something went wrong",'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		

######################### Function for sending notifiction to customer code


@csrf_exempt
def send_chatting_notification(token,title,body,data_message):
	try:
		device_token = token
		api_key = settings.API_KEY_NOTIFICATION
		push_service = FCMNotification(api_key=api_key)
		message_title = title
		message_body = body
		# message_icon = "mashwar_logo"
		# sound = "Default"
		color = "#FF22C19D"
		data_message = data_message
		print("device_token------>",device_token)
		push_service.single_device_data_message(registration_id=device_token,low_priority=False, data_message = data_message)
		send_data = "success"
	except Exception as e:
		print(str(traceback.format_exc()))
		# send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
		send_data = "error"
	return send_data
	
	
#################################################Getting list of message 


@csrf_exempt
def get_chatting_message_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		accept_user_id = data['accept_user_id']
		schedule_id = data['schedule_id']
		List = []
		Dict = {}
		
		if Chatting_Master.objects.filter(fk_user__id = user_id,fk_accept__id =accept_user_id,fk_pick_sched=schedule_id).exists():
			obj = Chatting_Master.objects.get(fk_user__id = user_id,fk_accept__id =accept_user_id,fk_pick_sched=schedule_id)
			
			message_obj = Chatting_Child.objects.filter(fk_chat_master__id = obj.id).order_by('date', 'time')
			for i in message_obj:
				Dict['message'] = i.message
				Dict['message_from'] = i.message_from
				Dict['date'] = i.date
				Dict['time'] = i.time.strftime('%H:%M')
				List.append(Dict)
				Dict = {}
				
			send_data = {'status':"1", 'msg':"Chatting Messages", 'chat':List}
			
		else:
			send_data = {'status':"1", 'msg':"Chatting Messages", 'chat':List}
		
	except Exception as e:
		print(str(traceback.format_exc()))
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
		
	return JsonResponse(send_data)
