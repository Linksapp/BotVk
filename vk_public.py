from cmath import inf
from dataclasses import field
from operator import ge
from webbrowser import get
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = '5f4851e6030f4d498493b024950c837cf1ce8ed6a5c21eef1ec235e877578a654480b58918442f4682388'
session = vk_api.VkApi(token=token)
vk = session.get_api()
longpoll = VkLongPoll(session, group_id=211021014)


def registration(id):
	'''
	Проверяет подписку на группу
	'''
	global members
	members = vk.groups.getMembers(group_id=211021014)['items']
	return id in members

def send_message(id, text):
	'''
	
	'''
	if isinstance(id, list):
		for _ in id:
			vk.messages.send(user_id=_, random_id=0, message=str(text))
	elif isinstance(id, int):
		vk.messages.send(user_id=id, random_id=0, message=str(text))

def get_info_about_member(id):
	info = {}
	# person_id = str(vk.users.get(user_ids = id)[0]['id'])
	info['id'] = vk.users.get(user_id = id)[0]['id']
	info['first_name'] = vk.users.get(user_id = id)[0]['first_name']
	info['last_name'] = vk.users.get(user_id = id)[0]['last_name']
	return info

print(get_info_about_member(208156464))


for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and registration(event.user_id) and event.to_me:
		send_message(event.user_id,'Hello')
		# send_message(event.user_id, get_info_about_member(event.user_id))
		# send_message(members, 'Рассылка подписчикам')


# USER_RECORDING_VOICE

