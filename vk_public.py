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


class VkBot:
	def __init__(self):
		self.session = vk_api.VkApi(token=token)
		self.vk = self.session.get_api()
		self.database = DataBase()

		self.longpoll = VkLongPoll(self.session, group_id=group_id)


	def create_user(self, id: int) -> None:
		"""Создает пользователя"""
		self.database.save_info(self.get_info_about_user(id))

	def registration(self, id: int) -> bool:
		"""Проверяет подписку"""
		return bool(self.vk.groups.isMember(group_id=group_id, user_id = id))

	def send_message(self, id: int, text: str = None, keyboard: dict = None, owner_id: str = '-211021014', 
					media_id: str = '457239017', attachment: str = None) -> None:
		"""Отправляет сообщения"""
		if attachment == 'photo':
			try:
				self.vk.messages.send(user_id = id, attachment = attachment + owner_id + '_' + media_id, random_id = 0, keyboard=keyboard)
			except Exception as error: print(error)
		else:
			try:
				self.vk.messages.send(user_id = id, message = str(text), random_id = 0, keyboard = keyboard)
			except Exception as error: print(error)

	def get_info_about_user(self, id: int) -> dict:
		"""Возвращает информацию о пользователе"""
		info = {}
		fields = ['id', 'first_name', 'last_name']
		try: 
			for _ in fields: info[_] = self.vk.users.get(user_id = id)[0][_]
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
	def take_keyboard(self, label: str) -> dict:
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

		if label == 'start': return start
		elif label == '/menu': return main_keyboard
		elif label == '/menu2': return menu_2
		else: return {}



	def bot_cycle(self):
		"""Longpoll цикл бота"""

		""" В database добавлена функция get_history вместо history для получения информации по кнопкам"""

		while True:
			for event in self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me:
					text: str = event.text.lower()
					if text == 'начать' and self.registration(event.user_id):
						self.send_message(event.user_id,'Hello', self.take_keyboard('/menu'))	
						self.create_user(event.user_id)
						self.database.change_history(event.user_id, '/menu')
						
					elif text == 'начать' and self.registration(event.user_id) == False: 
						self.send_message(event.user_id, 'Подпишись на группу!',  self.take_keyboard('start', False))
					
					if text == 'меню 2' and self.registration(event.user_id):
						self.send_message(event.user_id, 'Меню номер 2', self.take_keyboard('/menu2'))

					if text == 'назад':		
						self.send_message(event.user_id, 'Hello')
					
					if text == 'фото':
						self.send_message(event.user_id, attachment='photo', keyboard = self.take_keyboard('/menu2'))

					if event.user_id in admin_ids:		
						if text == 'exit()': sys.exit()

					# Сделать ответ на не команды 




if __name__ == "__main__":
	VkBot().bot_cycle()