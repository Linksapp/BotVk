import sys, time
import vk_api, database
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from user import User
from config import *
import json
#
"""Переделать архитектуру записи и чтения данных"""


def create_user(id: int, registration: bool) -> bool:
	"""Создает пользователя"""
	user = User(get_info_about_user(id), registration)
	if database.read_info(user.user_info): return True
	else: return False

def registration(id: int) -> bool:
	"""Проверяет подписку"""
	global members
	members = vk.groups.getMembers(group_id=211021014)['items']
	return id in members

def send_message(id: int | list, text: str, keyboard: dict = None):
	"""Отправляет сообщения"""
	# Добавить аргументы принимающие кнопки
	try:
		if isinstance(id, list):
			for _ in id: vk.messages.send(user_id=_, random_id=0, message=str(text))
		elif isinstance(id, int): vk.messages.send(user_id=id, random_id=0, message=str(text), keyboard=keyboard)
	except Exception as error: print(error)

def get_info_about_user(id: int) -> dict:
	"""Возвращает информацию о пользователе"""
	info = {}
	fields = ['id', 'first_name', 'last_name', 'domain']
	try:
		for _ in fields: info[_] = vk.users.get(user_id = id)[0][_]
		#print(json.dumps(info))
		return info
	except Exception as error:
		print('Def get_info_about_user', error)
		return info

def simple_keyboard(one_time: bool = False):
	keyboard = VkKeyboard(one_time=one_time)
	keyboard.add_button('Красная', color=VkKeyboardColor.NEGATIVE)
	keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
	return keyboard.get_keyboard()

def create_empty_keyboard():
	keyboard = VkKeyboard()
	return keyboard.get_empty_keyboard()

def bot_cycle():
	"""Longpoll цикл бота"""
	while True:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				text = event.text.lower()
				if text == 'начать':
					if registration(event.user_id): 
						keyboard = simple_keyboard()
						send_message(event.user_id,'Hello', keyboard=keyboard)	
						create_user(event.user_id, True)		# второй раз проверяет регистрацию
					elif registration(event.user_id) == False: 
						send_message(event.user_id, 'Подпишись на группу!')		# будет проверять только если введено "начать", надо или сбрасывать кнопку, или чтобы приветствие всегда было первым сообщением
				if text == 'красная':
					keyboard = simple_keyboard()
					send_message(event.user_id, 'Красная', keyboard=keyboard)		# Нужно найти способ вызывать клавиатуру без сообщений  
				if text == 'назад':
					# keyboard = simple_keyboard(True)
					# send_message(event.user_id, 'Вернулись', keyboard=keyboard)		# Клавиатура не пропадает, тк постоянно видит 'назад'
					keyboard = create_empty_keyboard()
					send_message(event.user_id, 'Вернулись', keyboard=keyboard)
				if event.user_id in admin_ids:			# убрал добавление не подписчика в базу
					if text == 'exit()': sys.exit()


if __name__ == "__main__":
	session = vk_api.VkApi(token=token)
	vk = session.get_api()

	longpoll = VkLongPoll(session, group_id=group_id)
	bot_cycle()