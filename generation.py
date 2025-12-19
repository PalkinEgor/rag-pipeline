import json
import pprint
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer

# Названия моделей
EMBEDDER_MODEL = 'intfloat/multilingual-e5-small'
GENERATION_MODEL = 'Qwen/Qwen3-1.7B'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Device: {DEVICE}')

# Загружаем модели
embedder_model = SentenceTransformer(EMBEDDER_MODEL).to(DEVICE)
tokenizer = AutoTokenizer.from_pretrained(GENERATION_MODEL)
model = AutoModelForCausalLM.from_pretrained(GENERATION_MODEL).to(DEVICE)

# Загружаем данные
with open('vector_db.json', 'r', encoding='utf-8') as f:
    vector_db = json.load(f)

# Косинусное сходство
def cos_compare(emb1, emb2):
    dot = np.dot(emb1, emb2)
    norm = np.linalg.norm(emb1) * np.linalg.norm(emb2)
    return 0.0 if norm == 0 else dot / norm

# Выбор лучших n чанков по запросу
def top_n(query, n=5):
    query_emb = embedder_model.encode(query, normalize_embeddings=True).tolist()
    result = []
    for item in vector_db:
        chunk = item[0]
        emb = item[1]
        cos_sim = cos_compare(query_emb, emb)
        result.append((chunk, float(cos_sim)))
    sorted_result = sorted(result, key=lambda x: x[1], reverse=True)
    return sorted_result[:n]

# Конструируем промпт обогащенный информацией
def prompt_builder(query, chunks):
    text = ''
    for chunk in chunks:
        text += chunk[0]
    prompt = f'''
Дай ответ на данный вопрос, используя информацию из текста:
{query}
Текст:
{text}
    '''
    return prompt

# Основная функция
def pipeline(query):
    # Запускаем rag
    chunks = top_n(query)
    new_query = prompt_builder(query, chunks)
    new_chunks = chunks + top_n(new_query, n=3)
    seen = set()
    unique_chunks = []
    for chunk, score in new_chunks:
        if chunk not in seen:
            unique_chunks.append((chunk, score))
            seen.add(chunk)

    # Формируем промпт
    query = prompt_builder(query, unique_chunks)
    messages = [
        {'role': 'system', 'content': 'Ты - экспертный ассистент. Отвечай ТОЛЬКО на основе предоставленного текста. Если в тексте нет ответа, скажи: "В тексте нет информации"'},
        {'role': 'user', 'content': query}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )

    # Токенизируем текст
    model_inputs = tokenizer([text], return_tensors='pt').to(DEVICE)
    prompt_len = model_inputs['input_ids'].shape[-1]
    
    # Генерация ответа
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )
    answer_ids = generated_ids[0][prompt_len:]
    answer = tokenizer.decode(answer_ids, skip_special_tokens=True)
    return answer


if __name__ == '__main__':
    while True:
        query = input('Ваш вопрос: ')
        if query == '0':
            break
        print(f'Ответ: {pipeline(query)}')
