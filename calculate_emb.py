import json
import pprint
from sentence_transformers import SentenceTransformer

# Читаем данные
with open('team.json', 'r', encoding='utf-8') as f:
    teams = json.load(f)
with open('pilot.json', 'r', encoding='utf-8') as f:
    pilot = json.load(f)
with open('grand_prix.json', 'r', encoding='utf-8') as f:
    grand_prix = json.load(f)
with open('circuit.json', 'r', encoding='utf-8') as f:
    circuit = json.load(f)

# Функция конструирующая предложение
def make_sentence(objects, translate):
    result = []
    for obj, features in objects.items():
        sentence = obj + '. '
        for key, value in features.items():
            if not isinstance(value, list):
                sentence += f'{translate[key]}: {value}. '
            else:
                sentence += f'{translate[key]}: {', '.join([i for i in value])}.'
        result.append(sentence)
    return result

# Составляем предложения для команд
team_translate = {
    'desc': 'Описание',
    'pilots': 'Пилоты',
    'sport_director': 'Спортивный директор',
    'team_principal': 'Руководитель команды',
    'year': 'Год основания'
}
teams_s = make_sentence(teams, team_translate)

# Составляем предложения для пилотов
pilot_translate = {
    'birth_date': 'Дата рождения',
    'champ': 'Чемпионств',
    'country': 'Страна',
    'desc': 'Описание',
    'podiums': 'Кол-во подиумов',
    'team': 'Команда'
}
pilots_s = make_sentence(pilot, pilot_translate)

# Составляем предложения для гран-при
grand_prix_translate = {
    'circuit': 'Трасса',
    'circuits': 'Кол-во кругов',
    'country': 'Страна',
    'date': 'Дата',
    'desc': 'Описание'
}
grand_prix_s = make_sentence(grand_prix, grand_prix_translate)

# Составляем предложения для трасс
circuit_translate = {
    'country': 'Страна',
    'desc': 'Описание',
    'length': 'Длина'
}
circuit_s = make_sentence(circuit, circuit_translate)

# Создаем ембеддинги
model = SentenceTransformer('intfloat/multilingual-e5-small')
team_embs = model.encode(teams_s, normalize_embeddings=True).tolist()
pilot_embs = model.encode(pilots_s, normalize_embeddings=True).tolist()
grand_prix_embs = model.encode(grand_prix_s, normalize_embeddings=True).tolist()
circuit_embs = model.encode(circuit_s, normalize_embeddings=True).tolist()

# Сохраняем результаты
result = []
for i in range(len(teams_s)):
    result.append((teams_s[i], team_embs[i]))
for i in range(len(pilots_s)):
    result.append((pilots_s[i], pilot_embs[i]))
for i in range(len(grand_prix_s)):
    result.append((grand_prix_s[i], grand_prix_embs[i]))
for i in range(len(circuit_s)):
    result.append((circuit_s[i], circuit_embs[i]))

with open('vector_db.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)