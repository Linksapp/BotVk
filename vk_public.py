import sys
import vk_api, database
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from config import *


"""Переделать архитектуру записи и чтения данных"""


def create_user(id: int) -> None:
	"""Создает пользователя"""
	user: dict = get_info_about_user(id)
	database.save_info(user)

def registration(id: int) -> bool:
	"""Проверяет подписку"""
	global members
	members = vk.groups.getMembers(group_id=211021014)['items']
	return id in members

def send_message(id: int, text: str, keyboard: dict = None) -> None:
	"""Отправляет сообщения"""
	# Добавить аргументы принимающие кнопки
	try:
		if keyboard == None: vk.messages.send(user_id = id, message = str(text), random_id = 0)
		else: vk.messages.send(user_id = id, message = str(text), random_id = 0, keyboard = keyboard)
	except Exception as error: print(error)

def get_info_about_user(id: int) -> dict:
	"""Возвращает информацию о пользователе"""
	info = {}
	fields = ['id', 'first_name', 'last_name', 'domain']
	try:
		for _ in fields: info[_] = vk.users.get(user_id = id)[0][_]
		return info
	except Exception as error:
		#print('Def get_info_about_user', error)
		return info

def create_empty_keyboard(one_time: bool = True):
	keyboard = VkKeyboard(one_time=one_time)
	return keyboard.get_empty_keyboard()

def create_main_keyboard(one_time: bool = True):
	color = {'зеленый': 'positive', 'красный': 'negative', 'синий': 'primary', 'белый': 'secondary'}
	keyboard = VkKeyboard(one_time=one_time)

	keyboard.add_button('Красная', color='negative')
	keyboard.add_button('Зелёная', color='positive')
	keyboard.add_button('Синяя', color='primary')
	keyboard.add_button('Белая', color='secondary')
	keyboard.add_line()
	keyboard.add_button('Меню 2')		
	return keyboard.get_keyboard()

def create_menu2_keyboard(one_time: bool = True):
	keyboard = VkKeyboard(one_time=one_time)
	keyboard.add_button('Фото', color='negative')
	keyboard.add_button('Назад')
	return keyboard.get_keyboard()

def create_start_keyboard(one_time: bool = True):
	keyboard = VkKeyboard(one_time=one_time)
	keyboard.add_button('Начать', color='primary')
	return keyboard.get_keyboard()

def bot_cycle():
	"""Longpoll цикл бота"""
	while True:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				text = event.text.lower()
				if text == 'начать' and registration(event.user_id): 
					send_message(event.user_id,'Hello', keyboard=create_main_keyboard())	
					create_user(event.user_id)		# второй раз проверяет регистрацию
				elif text == 'начать' and registration(event.user_id) == False: 
					send_message(event.user_id, 'Подпишись на группу!', keyboard=create_start_keyboard())
				if registration(event.user_id) and text == 'меню 2':
					send_message(event.user_id, 'Меню номер 2', keyboard=create_menu2_keyboard())
				if text == 'назад':
					send_message(event.user_id, 'ххххх')		# не работает. Надо понять как работать в пределах одной менюшки, чтобы нельзя было вызвать что-нибудь из других (например получить реакцию на 'начать' из 'меню2')
				if event.user_id in admin_ids:		
					if text == 'exit()': sys.exit()




if __name__ == "__main__":
	session = vk_api.VkApi(token=token)
	vk = session.get_api()
	database.init_json()

	longpoll = VkLongPoll(session, group_id=group_id)
	bot_cycle()