import re
import sys
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from user import User
from config import *


def create_user(id: int) -> bool:
	"""Создает пользователя"""
	user = User(get_info_about_user(id))
	if user.check_create(): return True
	else: return False

def registration(id: int) -> bool:
	"""Проверяет подписку"""
	global members
	members = vk.groups.getMembers(group_id=211021014)['items']
	if id in members: return True
	else: return False

def send_message(id: int | list, text: str):
	"""Отправляет сообщения"""
	if isinstance(id, list):
		for _ in id:
			vk.messages.send(user_id=_, random_id=0, message=str(text))
	elif isinstance(id, int):
		vk.messages.send(user_id=id, random_id=0, message=str(text))

def get_info_about_user(id: int) -> dict:
	"""Возвращает информацию о пользователе"""
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
	"""Longpoll цикл бота"""
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			text = event.text.lower()
			if text == 'начать':
				if registration(event.user_id): 
					send_message(event.user_id,'Hello')	
					create_user(event.user_id)		
				elif registration(event.user_id) == False: 
					send_message(event.user_id, 'Подпишись на группу!')		# будет проверять только если введено "начать", надо или сбрасывать кнопку, или чтобы приветствие всегда было первым сообщением
			if event.user_id in admin_ids:			# убрал добавление не подписчика в базу
				if text == 'exit()': sys.exit()

	


if __name__ == "__main__":
	session = vk_api.VkApi(token=token)
	vk = session.get_api()

	longpoll = VkLongPoll(session, group_id=211021014)
	bot_cycle()