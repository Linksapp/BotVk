import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from user import User
from config import *

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
	Отправляет сообщение
	'''
	if isinstance(id, list):
		for _ in id:
			vk.messages.send(user_id=_, random_id=0, message=str(text))
	elif isinstance(id, int):
		vk.messages.send(user_id=id, random_id=0, message=str(text))

def get_info_about_user(id):
	'''
	Возвращает информацию о пользователе 
	'''
	info = {}
	info['id'] = vk.users.get(user_id = id)[0]['id']
	info['first_name'] = vk.users.get(user_id = id)[0]['first_name']
	info['last_name'] = vk.users.get(user_id = id)[0]['last_name']
	return info



for event in longpoll.listen():
	text = event.text.lower()
	if text == 'начать':
		if event.type == VkEventType.MESSAGE_NEW and registration(event.user_id) and event.to_me:
			send_message(event.user_id,'Hello')
		# send_message(event.user_id, get_info_about_user(event.user_id))
		# send_message(members, 'Рассылка подписчикам')
		elif event.type == VkEventType.MESSAGE_NEW and registration(event.user_id) == False and event.to_me:
			send_message(event.user_id, 'Подпишись на группу')

# USER_RECORDING_VOICE


