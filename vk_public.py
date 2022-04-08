import sys
import vk_api
from database import DataBase
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from config import *


"""Переделать архитектуру записи и чтения данных"""
'''Функция для подписки'''

def create_user(id: int) -> None:
	"""Создает пользователя"""
	database.save_info(get_info_about_user(id))

def registration(id: int) -> bool:
	"""Проверяет подписку"""
	members = vk.groups.getMembers(group_id=211021014)['items']
	return id in members

def send_message(id: int, text: str = None, keyboard: dict = None, owner_id: str = '-211021014', 
				media_id: str = '457239017', attachment: str = None) -> None:
	"""Отправляет сообщения"""
	if attachment == 'photo':
		try:
			vk.messages.send(user_id = id, attachment = attachment + owner_id + '_' + media_id, random_id = 0, keyboard=keyboard)
		except Exception as error: print(error)
	else:
		try:
			vk.messages.send(user_id = id, message = str(text), random_id = 0, keyboard = keyboard)
		except Exception as error: print(error)

def get_info_about_user(id: int) -> dict:
	"""Возвращает информацию о пользователе"""
	info = {}
	fields = ['id', 'first_name', 'last_name']
	try:
		for _ in fields: info[_] = vk.users.get(user_id = id)[0][_]
		return info
	except Exception as error: return info


def keyboard(func): 
	def create_(one_time: bool = True):
		keyboard = VkKeyboard(one_time = one_time)
		func(keyboard)

	return create_

@keyboard
def create_empty_keyboard(keyboard):
	"""Создаёт пустую клавиатуру"""
	return keyboard.get_empty_keyboard()

def create_main_keyboard(one_time: bool = True):
	'''Создаёт главную клавиатуру'''
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
	'''Создаёт клавиатуру (Меню 2)'''
	keyboard = VkKeyboard(one_time=one_time)
	keyboard.add_button('Фото', color='negative')
	keyboard.add_button('Назад')
	return keyboard.get_keyboard()

def create_start_keyboard(one_time: bool = True):
	'''Создаёт начальную клавиатуру'''
	keyboard = VkKeyboard(one_time=one_time)
	keyboard.add_button('Начать', color='primary')
	return keyboard.get_keyboard()

def bot_cycle():
	keyboards: dict = {'main_menu': create_main_keyboard}
	"""Longpoll цикл бота"""

	""" В database добавлена функция get_history вместо history для получения информации по кнопкам"""

	history: list = [] # для хранения истории перехода между меню

	while True:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				text: str = event.text.lower()
				if text == 'начать' and registration(event.user_id):
					if 'main_menu' not in database.get_history(event.user_id): database.change_history(event.user_id, 'main_menu')

					if create_main_keyboard not in history: history.append(create_main_keyboard)
					send_message(event.user_id,'Hello', keyboard=keyboards['main_menu']())	
					create_user(event.user_id)
					
				elif text == 'начать' and registration(event.user_id) == False: 
					send_message(event.user_id, 'Подпишись на группу!', keyboard=create_start_keyboard())
				
				if text == 'меню 2' and registration(event.user_id) and len(history) == 1:
					if create_menu2_keyboard not in history: history.append(create_menu2_keyboard)
					send_message(event.user_id, 'Меню номер 2', keyboard=history[-1]())

				if text == 'назад' and len(history) > 1:		
					history.pop()
					send_message(event.user_id,'Hello', keyboard=history[-1]())
				
				if text == 'фото' and len(history) > 1:
					send_message(event.user_id, attachment='photo', keyboard=history[-1]())

				if event.user_id in admin_ids:		
					if text == 'exit()': sys.exit()

				# Сделать ответ на не команды




if __name__ == "__main__":
	session = vk_api.VkApi(token=token)
	vk = session.get_api()
	database = DataBase()

	longpoll = VkLongPoll(session, group_id=group_id)
	bot_cycle()