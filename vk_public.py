import sys
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from user import User
from config import *


def create_user(registration: bool) -> bool:
	user = User(get_info_about_user(id), registration)
	if user.check_create(): return True
	else: return False

def registration(id: int) -> bool:
	'''
	Проверяет подписку на группу
	'''
	global members
	members = vk.groups.getMembers(group_id=211021014)['items']
	return id in members

def send_message(id: int | list, text: str):
	'''
	Отправляет сообщение
	'''
	if isinstance(id, list):
		for _ in id:
			vk.messages.send(user_id=_, random_id=0, message=str(text))
	elif isinstance(id, int):
		vk.messages.send(user_id=id, random_id=0, message=str(text))

def get_info_about_user(id: int) -> dict:
	'''
	Возвращает информацию о пользователе 
	'''
	info = {}
	try:
		info['id'] = vk.users.get(user_id = id)[0]['id']
		info['first_name'] = vk.users.get(user_id = id)[0]['first_name']
		info['last_name'] = vk.users.get(user_id = id)[0]['last_name']
		return info
	except Exception as error:
		print(error)
		return info


def bot_cycle():
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			text = event.text.lower()
			if text == 'начать':
				if registration(event.user_id): 
					send_message(event.user_id,'Hello')
					create_user(True)
				# send_message(event.user_id, get_info_about_user(event.user_id))
				# send_message(members, 'Рассылка подписчикам')
				elif registration(event.user_id) == False: 
					send_message(event.user_id, 'Подпишись на группу!')
					create_user(False)
			if event.user_id in admin_ids:
				if text == 'exit()': sys.exit()

	# USER_RECORDING_VOICE


if __name__ == "__main__":
	session = vk_api.VkApi(token=token)
	vk = session.get_api()

	longpoll = VkLongPoll(session, group_id=211021014)
	bot_cycle()