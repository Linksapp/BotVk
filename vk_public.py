import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType    

token = '5f4851e6030f4d498493b024950c837cf1ce8ed6a5c21eef1ec235e877578a654480b58918442f4682388'
session = vk_api.VkApi(token=token)
vk = session.get_api()
longpoll = VkLongPoll(session, group_id=211021014)

#print(members)
def registration(id):
	members = vk.groups.getMembers(group_id=211021014)['items']
	return id in members
	
for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and registration(event.user_id) and event.to_me:
		vk.messages.send(user_id=event.user_id, random_id=0, message='Hello')
		

# USER_RECORDIN_VOICE


