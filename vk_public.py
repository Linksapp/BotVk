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
	try:
		vk.messages.send(user_id = id, message = str(text), random_id = 0, keyboard = keyboard)
	except Exception as error: print(error)

def send_photo(id: int, owner_id: str = '-211021014', media_id = '457239017', keyboard: dict = None ):
	try:
		vk.messages.send(user_id = id, attachment = 'photo' + owner_id + '_' + media_id, random_id = 0, keyboard=keyboard)
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
	"""Создаёт пустую клавиатуру"""
	keyboard = VkKeyboard(one_time=one_time)
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
	"""Longpoll цикл бота"""

	history: list = [] # для хранения истории перехода между меню

	while True:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				text: str = event.text.lower()
				if text == 'начать' and registration(event.user_id): 
					if create_main_keyboard not in history: history.append(create_main_keyboard)
					send_message(event.user_id,'Hello', keyboard=history[-1]())	
					create_user(event.user_id)		
					
				elif text == 'начать' and registration(event.user_id) == False: 
					send_message(event.user_id, 'Подпишись на группу!', keyboard=create_start_keyboard())
				
				if text == 'меню 2' and registration(event.user_id) and len(history) == 1:
					if create_menu2_keyboard not in history: history.append(create_menu2_keyboard)
					send_message(event.user_id, 'Меню номер 2', keyboard=history[-1]())

				if text == 'назад' and len(history) > 1:		# )))))))
					history.pop()
					send_message(event.user_id,'Hello', keyboard=history[-1]())
				
				if text == 'фото' and len(history) > 1:
					send_photo(event.user_id, keyboard=history[-1]())

				if event.user_id in admin_ids:		
					if text == 'exit()': sys.exit()

				# Сделать ответ на не команды




if __name__ == "__main__":
	session = vk_api.VkApi(token=token)
	vk = session.get_api()
	database.init()

	longpoll = VkLongPoll(session, group_id=group_id)
	bot_cycle()
