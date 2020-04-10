from django.conf.urls import url, include
from .views import *
from .views_web import *

urlpatterns = [
	url(r'^user_signup_web/$', user_signup_web, name='user_signup_web'),
	url(r'^user_login_web/$', user_login_web, name='user_login_web'),
	url(r'^user_change_password_web/$', user_change_password_web, name='user_change_password_web'),
	url(r'^user_list_web/$', user_list_web, name='user_list_web'),
	url(r'^user_list_by_id_web/$', user_list_by_id_web, name='user_list_by_id_web'),
	url(r'^create_group_web/$', create_group_web, name='create_group_web'),
	url(r'^group_list_web/$', group_list_web, name='group_list_web'),
	url(r'^forget_password_web/$', forget_password_web, name='forget_password_web'),
	url(r'^save_schedule_web/$', save_schedule_web, name='save_schedule_web'),
	url(r'^get_schedule_web/$', get_schedule_web, name='get_schedule_web'),
	url(r'^delete_schedule_web/$', delete_schedule_web, name='delete_schedule_web'),
	url(r'^schedule_list_for_gruop_web/$', schedule_list_for_gruop_web, name='schedule_list_for_gruop_web'),
	url(r'^accept_schedule_web/$', accept_schedule_web, name='accept_schedule_web'),
	url(r'^accept_schedule_list_web/$', accept_schedule_list_web, name='accept_schedule_list_web'),
	url(r'^save_pickup_info_web/$', save_pickup_info_web, name='save_pickup_info_web'),
	url(r'^group_member_list_web/$', group_member_list_web, name='group_member_list_web'),
	url(r'^update_user_profile_web/$', update_user_profile_web, name='update_user_profile_web'),
	url(r'^change_password/$', change_password, name='change_password'),
	url(r'^save_chatting_message_web/$', save_chatting_message_web, name='save_chatting_message_web'),
	url(r'^send_chatting_notification/$', send_chatting_notification, name='send_chatting_notification'),
	url(r'^get_chatting_message_web/$', get_chatting_message_web, name='get_chatting_message_web'),
	url(r'^update_tooken_web/$', update_tooken_web, name='update_tooken_web'),

]
