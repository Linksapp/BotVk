import sys
import vk_api
import time
from database import DataBase
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from config import *


"""Переделать архитектуру записи и чтения данных"""
'''Функция для подписки'''

def test_time(func):
	def test(a=None):
		start = time.time()
		func(a)
		finish = time.time()
		print(finish - start)
	return test

def create_user(id: int) -> None:
	"""Создает пользователя"""
	database.save_info(get_info_about_user(id))

def registration(id: int) -> bool:
	"""Проверяет подписку"""
	# использовать метод isMembers
	member: bool = vk.groups.isMember(group_id=group_id, user_id = id)
	return member

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
	except Exception as error: print(error)
	return info


""" В голове выглядело как крутая идея, на деле написал хуйню, переписать"""

def keyboard(func): 
	"""Декоратор для создания клавиатуры"""
	def create_(label: str = None, one_time: bool = True) -> str:
		keyboard = VkKeyboard(one_time = one_time)
		response: dict = func(label)

		if response == {}: keyboard.get_empty_keyboard()
		else:
			for i in response:
				if response.get(i) == None: keyboard.add_line()
				else: keyboard.add_button(i, response.get(i))

		return keyboard.get_keyboard()

	return create_

@keyboard
def take_keyboard(label: str) -> dict:
	#color = {'зеленый': 'positive', 'красный': 'negative', 'синий': 'primary', 'белый': 'secondary'}
	# Buttons
	start = {'Начать': 'positive'}

	menu_2 = {
		'Фото': 'negative',
		'Назад': 'secondary'
	}

	main_keyboard = {
		'Красная': 'negative', 
		'Зеленая': 'positive', 
		'Синяя': 'primary', 
		'Белая': 'secondary', 
		'': None,
		'Меню 2': 'secondary'
	}

	if label == 'начать': return start
	elif label == 'меню': return main_keyboard
	elif label == 'меню2': return menu_2
	else: return {}



def bot_cycle():
	"""Longpoll цикл бота"""

	""" В database добавлена функция get_history вместо history для получения информации по кнопкам"""

	while True:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				text: str = event.text.lower()
				if text == 'начать' and registration(event.user_id):
					#if 'main_menu' not in database.get_history(event.user_id): database.change_history(event.user_id, 'main_menu')
					send_message(event.user_id,'Hello', take_keyboard('меню'))	
					create_user(event.user_id)
					
				elif text == 'начать' and registration(event.user_id) == False: 
					send_message(event.user_id, 'Подпишись на группу!',  take_keyboard('начать'))
				
				if text == 'меню 2' and registration(event.user_id):
					send_message(event.user_id, 'Меню номер 2', take_keyboard('меню2'))

				if text == 'назад':		
					send_message(event.user_id, 'Hello')
				
				if text == 'фото':
					send_message(event.user_id, attachment='photo')

				if event.user_id in admin_ids:		
					if text == 'exit()': sys.exit()

				# Сделать ответ на не команды 




if __name__ == "__main__":
	session = vk_api.VkApi(token=token)
	vk = session.get_api()
	database = DataBase()

	longpoll = VkLongPoll(session, group_id=group_id)
	bot_cycle()