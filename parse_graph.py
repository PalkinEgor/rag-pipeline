import json
import pprint

# Читаем данные
with open('graph.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
nodes = data['nodes']
arcs = data['arcs']
object_label = 'http://www.w3.org/2000/01/rdf-schema#label'


# Функция для парсинга
def get_objects(objects_name, features):
    result = {}
    for node in nodes:
        for obj in objects_name:
            if obj in node['data'][object_label][0].replace('@ru', ''):
                current_dict = {}
                for feature in features.keys():
                    try:
                        current_dict[feature] = node['data']['params_values'][features[feature]]
                    except KeyError:
                        current_dict[feature] = None
                result[obj] = current_dict
    return result

# Парсим команды
teams = ['Alpine', 'Aston Martin', 'Ferrari', 'Haas', 'Kick Sauber', 
         'McLaren', 'Mercedes', 'Racing Bulls', 'Red Bull Racing', 'Williams']
teams_features = {
    'year': 'http://erlangen-crm.org/mainOntology/0db9f232-e4a9-4f69-830e-b33b52336f39/2cdc4782-f400-4029-a1ad-b631d681a6d2',
    'desc': 'http://www.w3.org/2000/01/rdf-schema#comment'
}
teams_dict = get_objects(teams, teams_features)

# Парсим пилотов
pilots = ['Айзек Хаджар', 'Александр Албон', 'Габриель Бортолето', 'Джордж Рассел', 'Карлос Сайнц', 'Кими Антонелли',
          'Ландо Норрис', 'Лиам Лоусон', 'Льюис Хэмилтон', 'Лэнс Стролл', 'Макс Ферстаппен', 'Нико Хюкельберг', 'Оливер Берман',
          'Оскар Пиастри', 'Пьер Гасли', 'Фернандо Алонсо', 'Франко Колапинто', 'Шарль Леклер', 'Эстебан Окон', 'Юки Тсунода']
pilots_features = {
    'birth_date': 'http://erlangen-crm.org/mainOntology/0db9f232-e4a9-4f69-830e-b33b52336f39/a6ff7784-c841-4381-aef3-f54fdbb2cffb',
    'desc': 'http://www.w3.org/2000/01/rdf-schema#comment', 
    'podiums': 'http://erlangen-crm.org/mainOntology/0db9f232-e4a9-4f69-830e-b33b52336f39/8e327aa4-fe7a-4807-88ab-8fea63f5766a',
    'champ': 'http://erlangen-crm.org/mainOntology/0db9f232-e4a9-4f69-830e-b33b52336f39/587d0e69-f6bc-43f9-b564-4af56c5c1fa7'
}
pilots_dict = get_objects(pilots, pilots_features)

# Парсим Гран-при
grand_prix = ['Гран-при Абу-Даби', 'Гран-при Австралии', 'Гран-при Австрии', 'Гран-при Азербайджана', 'Гран-при Бахрейна', 'Гран-при Бельгии', 'Гран-при Великобритании', 
              'Гран-при Венгрии', 'Гран-при Испании', 'Гран-при Италии', 'Гран-при Канады', 'Гран-при Катара', 'Гран-при Китая', 'Гран-при Лас-Вегаса', 'Гран-при Майами',
              'Гран-при Мехико', 'Гран-при Монако', 'Гран-при Нидерландов', 'Гран-при Сан-Паулу', 'Гран-при Саудовской Аравии', 'Гран-при Сингапура', 'Гран-при США', 
              'Гран-при Эмилии-Романьи', 'Гран-при Японии']
grand_prix_features = {
    'circuits': 'http://erlangen-crm.org/mainOntology/0db9f232-e4a9-4f69-830e-b33b52336f39/bd5da65d-9e40-4e4b-9bde-60c7101981d0',
    'date': 'http://erlangen-crm.org/mainOntology/0db9f232-e4a9-4f69-830e-b33b52336f39/c78bee05-279b-45f2-ace1-d66f931d3302',
    'desc': 'http://www.w3.org/2000/01/rdf-schema#comment'
}
grand_prix_dict = get_objects(grand_prix, grand_prix_features)

# Парсим Трассы
circuits = ['Автодром Барселона-Каталония', 'Альберт парк', 'Автодром братьев Родригес', 'Автодром Энцо и Дино Феррари', 'Баку', 'Джидда', 'Интерлагос', 'Лас-Вегас', 
            'Лусаил', 'Марина-Бэй', 'Международный автодром Бахрейна', 'Международный автодром Майами', 'Монако', 'Монца', 'Ред Булл Ринг', 'Спа-Франкоршам', 'Сузука', 
            'Трасса Америк', 'Трасса Жиль-Вильнев', 'Трасса Зандворт', 'Трасса Сильверстоун', 'Хунгароринг', 'Шанхайский Международный Автодром', 'Яс-Марина']
circuits_features = {
    'length': 'http://erlangen-crm.org/mainOntology/0db9f232-e4a9-4f69-830e-b33b52336f39/dc87dbc9-404c-4467-ad77-83f60cd9b2a6',
    'desc': 'http://www.w3.org/2000/01/rdf-schema#comment'
}
circuits_dict = get_objects(circuits, circuits_features)

# Парсим спортивных директоров и руководителей команд
sport_directors = []
team_principal = []
for arc in arcs:
    end_node = arc['data']['end_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    start_node = arc['data']['start_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    if end_node[0] == 'Спортивный директор@ru':
        if start_node[0].replace('@ru', '') not in ['Команда', 'Год начала работы', 'Имя']:
            sport_directors.append(start_node[0].replace('@ru', ''))
    if end_node[0] == 'Руководитель команды@ru':
        if start_node[0].replace('@ru', '') not in ['Команда', 'Текущий руководитель', 'Год начала работы', 'Имя']:
            team_principal.append(start_node[0].replace('@ru', ''))

# Добавляем спортивного директора и руководителя команды в команду
for arc in arcs:
    end_node = arc['data']['end_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    start_node = arc['data']['start_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    for tp in team_principal:        
        if start_node[0].replace('@ru', '') == tp:
            team = end_node[0].replace('@ru', '')
            if team in teams:
                teams_dict[team]['team_principal'] = tp
                break
    for sd in sport_directors:
        if start_node[0].replace('@ru', '') == sd:
            team = end_node[0].replace('@ru', '')
            if team in teams:
                teams_dict[team]['sport_director'] = sd
                break

# Добавляем команду и страну пилотам
for arc in arcs:
    end_node = arc['data']['end_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    start_node = arc['data']['start_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    for pilot in pilots:
        if start_node[0].replace('@ru', '') == pilot:
            team = end_node[0].replace('@ru', '')
            if team in teams:
                pilots_dict[pilot]['team'] = team
                break
            else:
                country = end_node[0].replace('@ru', '')
                if country != 'Пилот':
                    pilots_dict[pilot]['country'] = country
                    break

# Добавляем политов командам
for team in teams:
    current_pilots = []
    for pilot in pilots_dict.keys():
        if pilots_dict[pilot]['team'] == team:
            current_pilots.append(pilot)
    teams_dict[team]['pilots'] = current_pilots

# Добавляем страну трассам
for arc in arcs:
    end_node = arc['data']['end_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    start_node = arc['data']['start_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    for c in circuits:
        if start_node[0].replace('@ru', '') == c:
            if end_node[0] not in ['Трасса@ru', 'Страна@ru']:
                country = end_node[0].replace('@ru', '')
                circuits_dict[c]['country'] = country
                break

# Добавляем трассу и страну гран-при
for arc in arcs:
    end_node = arc['data']['end_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    start_node = arc['data']['start_node']['data']['http://www.w3.org/2000/01/rdf-schema#label']
    for gp in grand_prix:
        if start_node[0].replace('@ru', '') == gp:
            circuit = end_node[0].replace('@ru', '')
            if circuit in circuits:
                grand_prix_dict[gp]['circuit'] = circuit
                break
            else:
                country = end_node[0].replace('@ru', '')
                if country != 'Гран-при':
                    grand_prix_dict[gp]['country'] = country
                    break

# Сохраняем результаты
with open('team.json', 'w', encoding='utf-8') as f:
    json.dump(teams_dict, f)
with open('pilot.json', 'w', encoding='utf-8') as f:
    json.dump(pilots_dict, f)
with open('grand_prix.json', 'w', encoding='utf-8') as f:
    json.dump(grand_prix_dict, f)
with open('circuit.json', 'w', encoding='utf-8') as f:
    json.dump(circuits_dict, f)