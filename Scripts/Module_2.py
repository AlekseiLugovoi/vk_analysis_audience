
import datetime
import requests
import pandas as pd


# Сервисный ключ доступа
access_token = '****'


def url_request(id, field="none"):
    url = 'https://api.vk.com/method/users.get?user_id={}&fields={}&v=5.8&' \
          'access_token=%s' % access_token
    json_data = requests.get(url.format(id, field)).json()
    return json_data


def age(id):
    bdate_data = url_request(id, 'bdate')
    try:
        age = datetime.datetime.now().year - int(bdate_data['response'][0]['bdate'][-4:])
    except ValueError:
        return "не указано"
    except KeyError:
        return "не указано"
    return age


def city(id):
    city_data = url_request(id, 'city')
    try:
        return city_data['response'][0]['city']['title']
    except KeyError:
        return 'не указано'


def connections(id):
    connections_data = url_request(id, 'connections')
    connections_dict = {'skype':       'none',
                        'facebook':    'none',
                        'twitter':     'none',
                        'livejournal': 'none',
                        'instagram':   'none'}
    for connection in connections_dict.keys():
        if connection in connections_data['response'][0].keys():
            connections_dict.update({connection: connections_data['response'][0][connection]})
    return connections_dict


def domain(id):
    domain_data = url_request(id, 'domain')
    return domain_data['response'][0]['domain']


def name(id):
    name_data = url_request(id)
    first_name = name_data['response'][0]['first_name']
    last_name = name_data['response'][0]['last_name']
    return last_name + ' ' + first_name


def gender(id):
    gender_data = url_request(id, 'sex')
    gender_dict = {1: 'женский',
                   2: 'мужской',
                   0: 'пол не указан'}
    return gender_dict[gender_data['response'][0]['sex']]


def online(id):
    online_data = url_request(id, 'online')
    if online_data['response'][0]['online'] == 1:
        return 'online'
    else:
        return 'offline'


def relation(id):
    relation_data = url_request(id, 'relation')
    relation_dict = {1: 'не женат/не замужем',
                     2: 'есть друг/есть подруга',
                     3: 'помолвлен/помолвлена',
                     4: 'женат/замужем',
                     5: 'всё сложно',
                     6: 'в активном поиске',
                     7: 'влюблён/влюблена',
                     8: 'в гражданском браке',
                     0: 'не указано'}
    try:
        relation_value = relation_data['response'][0]['relation']
        return relation_dict[relation_value]
    except KeyError:
        return 'не указано'


def dataframe(id):
    df_dict = {'Короткий адрес страницы':           domain(id),
               'Имя':                                 name(id),
               'Пол':                               gender(id),
               'Возраст':                              age(id),
               'Город':                               city(id),
               'Семейное положение':              relation(id),
               'Skype':               connections(id)['skype'],
               'Facebook':         connections(id)['facebook'],
               'Twitter':           connections(id)['twitter'],
               'Livejournal':   connections(id)['livejournal'],
               'Instagram':      connections(id)['instagram']}

    df = pd.DataFrame(df_dict, index=[id], columns=df_dict.keys(), )
    df.index.name = 'id'
    return df


def get_friends(id):
    url = 'https://api.vk.com/method/friends.get?user_id={}&v=5.8&access_token=%s' % access_token
    json_data = requests.get(url.format(id)).json()
    return json_data['response']['items']


def main():
    user_id = int(input("id интересующего пользователя: "))

    friends = get_friends(user_id)
    df = pd.DataFrame()
    k = 0
    for friend in friends:
        df = df.append(dataframe(friend))
        k += 1
        print(k)
    print(df.head())
    # df.to_csv('Статистика.csv', sep=',', encoding='cp1251')


if __name__ == '__main__':
    main()


