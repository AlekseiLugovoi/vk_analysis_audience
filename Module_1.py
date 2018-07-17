
import datetime
from collections import Counter
import requests
import networkx as nx
import matplotlib.pyplot as plt


# Сервисный ключ доступа
access_token = '***'


# взаимосвязь друзей пользователя между собой
def relations(user_id):
    dic = {}
    friend_ids = get_friends(user_id)
    for friend in friend_ids:
        ids = get_friends(friend)
        dic[friend] = {i for i in ids if i in friend_ids}
    return dic, friend_ids


# url запрос + access_token
def get_friends(user_id):
    url = 'https://api.vk.com/method/friends.get?user_id={}&v=5.8&access_token=%s' % access_token
    return request_vk(user_id, url, islist=False)


# запрос к вк
def request_vk(items, url, islist=True):
    json_response = requests.get(url.format(items)).json()
    if islist == False:
        if json_response.get('error'):
            return set()
        return set(json_response['response']['items'])
    else:
        if json_response.get('error'):
            return list()
        return json_response['response']


def transform_to_graph(dic, f_ids):
    g = nx.Graph(directed=False)
    for i in dic:
        g.add_node(i)
        for j in dic[i]:
            if i != j and i in f_ids and j in f_ids:
                g.add_edge(i, j)
    return g


# url запрос + access_token
def get_user_info(user_id):
    url = 'https://api.vk.com/method/users.get?user_id={}&fields=sex,bdate,city,relation&v=5.8&access_token=%s' % access_token
    return request_vk(user_id, url)


def change_keys(d, a):
    for i, j in enumerate(a):
        if i in d:
            d[j] = d.pop(i)
    return d


# -------------------------------------------------- графика

# для выделения бОльшей части на круг.диаграмме
def make_explode(list):
    newlist = []
    max_index = list.index(max(list))
    for i in range(len(list)):
        if i == max_index:
            newlist.append(0.1)
        else:
            newlist.append(0)
    explode = tuple(newlist)
    return explode


def make_labels_and_sizes(dic):
    labels = [i for i in dic]
    sizes = [dic[i] for i in dic]
    return labels,  sizes


def make_pie(labels, sizes, title):
    explode = make_explode(sizes)
    if len(labels) < 5:
        plt.pie(sizes, explode=explode, labels=labels,
                autopct='%1.1f%%', startangle=140, pctdistance=0.7)
        plt.legend(title=title)
    else:
        patches, texts = plt.pie(sizes, startangle=140, explode=explode)
        plt.legend(patches, labels, loc="best", title=title)
        plt.tight_layout()
    plt.axis('equal')
    #plt.savefig('{}.png'.format(title), dpi=600)
    plt.show()


def main():
    user_id = int(input('id интересующего пользователя: '))
    dic, friend_ids = relations(user_id)
    G = transform_to_graph(dic, friend_ids)

    pos = nx.nx_pydot.graphviz_layout(G, prog="neato")
    nx.draw(G, pos, node_size=30, with_labels=False, width=0.2)
    plt.savefig('graph.png', dpi=600)
    plt.show()

    trans = {'Name': 'Имя',
             'Type': 'Тип',
             'Number of nodes': 'Число узлов',
             'Number of edges': 'Число дуг',
             'Average degree': 'Средняя степень'}

    info = nx.info(G)

    for k, v in trans.items():
        if k in info:
            info = info.replace(k, v)

    # отсечь "Имя графа"
    print(info[4:])

    res = {'sex': [],
           'rel': [],
           'dat': [],
           'loc': []}

    data = dict()

    curr_year = datetime.datetime.now().year
    y = str(curr_year % 200)

    # формирование списков параметров
    for userid in friend_ids:
        data[userid] = get_user_info(userid)
        q = data[userid][0]
        res['sex'].append(int(q.get('sex', 0)))
        res['rel'].append(int(q.get('relation', 0)))
        if 'bdate' in q and len(q['bdate']) > 5:
            res['dat'].append(datetime.datetime.now().year - int(q['bdate'][-4:]))
        else:
            res['dat'].append(0)
        if 'city' in q:
            res['loc'].append(q['city']['title'])
        else:
            res['loc'].append(0)

    # список значений
    gender = res['sex']
    relation = res['rel']
    age = res['dat']
    location = res['loc']

    # подсчет значений
    gender_count = dict(Counter(gender))
    relation_count = dict(Counter(relation))
    age_count = dict(Counter(age))
    location_count = dict(Counter(location))

    # замена в параметре "пол" 0: не указано, 1: жен, 2: муж
    gender_count = change_keys(gender_count, ['не указано',
                                              'жен',
                                              'муж'])

    relation_count = change_keys(relation_count, ['не указано',
                                                  'не женат/не замужем',
                                                  'есть друг/есть подруга',
                                                  'помолвлен/помолвлена',
                                                  'женат/замужем',
                                                  'все сложно',
                                                  'в активном поиске',
                                                  'влюблен/влюблена',
                                                  'в гражданском браке'])
    # фильтр выбросов
    age_count = change_keys(dict((k, v)
                                 for (k, v) in age_count.items()
                                 if k < 100),
                            ['не указано'])

    location_count = change_keys(dict((k, v)
                                      for (k, v) in location_count.items()
                                      if v > 1),
                                 ['не указано'])

    print("\n Пол: \n %s" % gender_count, '\n',
          "Семейное положение: \n %s" % relation_count, '\n',
          "Возраст: \n %s" % age_count, '\n',
          "Город: \n %s" % location_count, '\n')

    labels, sizes = make_labels_and_sizes(gender_count)
    make_pie(labels, sizes, "Пол")  # ok
    labels, sizes = make_labels_and_sizes(relation_count)
    make_pie(labels, sizes, "Семейное положение")  # !ok
    labels, sizes = make_labels_and_sizes(age_count)
    make_pie(labels, sizes, "Возраст")  # !ok
    labels, sizes = make_labels_and_sizes(location_count)
    make_pie(labels, sizes, "Место проживания")  # ok


if __name__ == '__main__':
    main()


