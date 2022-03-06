import vk_api, datetime

tokens = ['1e309e703f5c66ed5dde6cc3879c990ec2a7c719f61705a8a551d269d3fbca30adc83a38e56425df69c27', 
"91fb2cd0a39eaf26bec2472cb0d7668722637c76f461e652ae88a12f3316264f8f7bc1f2897685585211b",] 
groups_id = [63, 405]


def get_api(tokens):

    base = []
    for tok in tokens:
        session = vk_api.VkApi(token = tok)
        base.append(session.get_api())

    return base # active tokens

def send(msg = '+', tokens = None):

    """i = 0
    for token in tokens:
        group_id = token.messages.searchConversations(q = "Название группы", count = 1, field = 'id')['items'][0]['peer']['local_id']
        token.messages.send(chat_id = group_id, message = msg, random_id = 0)
        i += 1"""
        

    tokens[1].messages.send(chat_id = 405, message = msg, random_id = 0)
    tokens[0].messages.send(chat_id = 63, message = f'Было отправленно сообщений {1} в {get_now_time()}', random_id = 0)

def get_now_time():

    delta = datetime.timedelta(hours = 3, minutes = 0) # разница от UTC. Можете вписать любое значение вместо 3
    t = (datetime.datetime.now(datetime.timezone.utc) + delta) # Присваиваем дату и время переменной «t»

    nowtime = t.strftime("%H:%M") # текущее время
    nowdate = t.strftime("%d.%m.%Y") # текущая дата

    return [nowtime, nowdate]

def main(tokens):

    need_time = ['08:00', '11:54']
    pause = False
    while True:
        if pause != True and get_now_time()[0] in need_time:
            send(tokens = tokens)
            pause = True
        if pause and get_now_time()[0] == '00:00':
            pause = False


if __name__ == "__main__":
    main(get_api(tokens))
    

