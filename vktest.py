import vk_api
import time
token = '0c0359c5b83614671e81b696d9b9d6a1ff65cc9bae7560ed0377326d0a4c0a81b258583ffaff92421459f'
session = vk_api.VkApi(token=token)
vk = session.get_api()

a = vk.messages.send(user_id=376919311,random_id=0, message='message')
print(a)
time.sleep(2)
vk.messages.delete(message_ids=a, delete_for_all=1)
