import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize
import os

nltk.download('punkt')

# Загружаем модель
model_name = "cointegrated/rubert-tiny-sentiment-balanced"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def get_sentiment(text):
    """Функция для сентимент-анализа текста."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = softmax(outputs.logits[0].numpy())
    labels = ['negative', 'neutral', 'positive']
    return scores, labels[scores.argmax()]

def perform_sentiment_analysis(file_path, results_folder):
    """Функция для выполнения сентимент-анализа текста."""
    # Чтение и разбиение текста
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = sent_tokenize(text, language='russian')
    df = pd.DataFrame({'text': sentences})

    # Анализ каждой строки
    results = df['text'].apply(lambda x: get_sentiment(x))
    df[['negative', 'neutral', 'positive']] = pd.DataFrame(results.map(lambda x: x[0]).tolist(), index=df.index)
    df['predicted_label'] = results.map(lambda x: x[1])

    # Получаем имя канала из пути файла
    channel_name = os.path.basename(file_path).split('_preserved')[0]
    channel_name_clean = channel_name.strip().replace(" ", "_").lower()

    # Создаём только ту папку, которая пришла как results_folder
    os.makedirs(results_folder, exist_ok=True)

    # График
    label_counts = df['predicted_label'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    label_counts.plot(kind='bar', ax=ax, color=['red', 'gray', 'green'])
    ax.set_title('Распределение меток сентимента')
    ax.set_xlabel('Метка сентимента')
    ax.set_ylabel('Количество предложений')
    for i, freq in enumerate(label_counts):
        ax.text(i, freq, str(freq), ha='center', va='bottom')

    # Сохраняем график в папку канала
    sentiment_plot_path = os.path.join(results_folder, f"{channel_name_clean}_sentiment_plot.png")
    plt.savefig(sentiment_plot_path)
    plt.close()

    return sentiment_plot_path
