import os
import spacy
import matplotlib.pyplot as plt
from collections import Counter


def generate_entities_plot(file_path, results_folder):
    nlp = spacy.load("ru_core_news_sm")
    """Функция для извлечения сущностей и построения графика их частоты."""
    # Извлекаем имя телеграм-канала из пути файла (например, название файла без расширения)
    channel_name = os.path.splitext(os.path.basename(file_path))[0]

    # Создаем папку для результатов, если её нет
    os.makedirs(results_folder, exist_ok=True)

    # Читаем текст из выбранного файла
    with open(file_path, "r", encoding="utf-8") as f:
        cleaned_text = f.read()

    # Разбиваем текст на предложения
    texts = cleaned_text.split('.')

    # Список для хранения сущностей
    entities = []
    for text in texts:
        doc = nlp(text.strip())
        entities.extend([ent.label_ for ent in doc.ents])

    # Подсчет частоты сущностей
    entity_counts = Counter(entities)

    # График для поименованных сущностей
    if entity_counts:
        entity_labels, entity_counts_vals = zip(*entity_counts.most_common())
        plt.figure(figsize=(10, 6))
        plt.bar(entity_labels, entity_counts_vals)
        plt.xticks(rotation=45)
        plt.xlabel('Сущности')
        plt.ylabel('Частота')
        plt.title('Распределение поименованных сущностей')

        # Сохраняем график в папку результатов
        graph_filename = os.path.join(results_folder, f"{channel_name}_entities.png")
        plt.tight_layout()
        plt.savefig(graph_filename)
        plt.close()
    else:
        print("Поименованные сущности не найдены.")
