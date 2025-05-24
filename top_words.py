import os
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from collections import Counter

def generate_topwords_plot(cleaned_file_path, results_folder):
    """Строит график топ-30 слов на основе уже очищенного текста."""

    # Чтение очищенного текста
    with open(cleaned_file_path, 'r', encoding='utf-8') as f:
        cleaned_text = f.read()

    # Разбиваем текст на слова
    words = cleaned_text.split()

    # Подсчет частоты слов
    word_counts = Counter(words)

    # Топ 30 слов
    top_30_words = word_counts.most_common(30)

    if not top_30_words:
        print("Нет слов для отображения.")
        return

    # График
    words, counts = zip(*top_30_words)
    plt.figure(figsize=(12, 8))
    plt.bar(words, counts)
    plt.xticks(rotation=90)
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title('Топ 30 самых частых слов')
    plt.tight_layout()

    # Сохраняем график
    output_filename = "top_words_plot.png"
    output_path = os.path.join(results_folder, output_filename)
    plt.savefig(output_path)
    plt.close()

    print(f"График для топ 30 слов сохранен: {output_path}")
