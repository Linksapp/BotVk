import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = '5f4851e6030f4d498493b024950c837cf1ce8ed6a5c21eef1ec235e877578a654480b58918442f4682388'
session = vk_api.VkApi(token=token)
vk = session.get_api()
longpoll = VkLongPoll(session, group_id=211021014)


def registration(id):
	global members
	members = vk.groups.getMembers(group_id=211021014)['items']
	return id in members

def send_message(id, text):
	print(type(id))
	if isinstance(id, list):
		print('list')
		for _ in id:
			vk.messages.send(user_id=_, random_id=0, message=text)
	elif isinstance(id, int):
		vk.messages.send(user_id=id, random_id=0, message=text)

for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and registration(event.user_id) and event.to_me:
		send_message(event.user_id,'Hello')
		# send_message(members, 'Рассылка подписчикам')


# USER_RECORDING_VOICE


