import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType    

token = '5f4851e6030f4d498493b024950c837cf1ce8ed6a5c21eef1ec235e877578a654480b58918442f4682388'
session = vk_api.VkApi(token=token)
vk = session.get_api()
longpoll = VkLongPoll(session, group_id=211021014)

for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW:
		print(longpoll.listen())
		print(event.user_id)
		print(event.text)

print('aaaa')