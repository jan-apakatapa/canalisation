import os
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize

# Не загружаем pandas, torch и transformers на уровне модуля!
# nltk.download('punkt') лучше запускать 1 раз вручную

def load_sentiment_model():
    """Ленивая загрузка модели и токенизатора только при первом вызове."""
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from scipy.special import softmax

    model_name = "cointegrated/rubert-tiny-sentiment-balanced"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()
    return tokenizer, model, softmax

tokenizer = model = softmax = None

def get_sentiment(text):
    global tokenizer, model, softmax
    if tokenizer is None or model is None or softmax is None:
        tokenizer, model, softmax = load_sentiment_model()
        import torch  # повторный импорт для уверенности

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = softmax(outputs.logits[0].numpy())
    labels = ['negative', 'neutral', 'positive']
    return scores, labels[scores.argmax()]

def perform_sentiment_analysis(file_path, results_folder):
    # Чтение и разбиение текста
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = sent_tokenize(text, language='russian')

    # Анализируем по предложениям:
    predicted_labels = []
    label_counts = {'negative': 0, 'neutral': 0, 'positive': 0}

    for sent in sentences:
        _, label = get_sentiment(sent)
        predicted_labels.append(label)
        label_counts[label] += 1

    # Получаем имя канала из пути файла
    channel_name = os.path.basename(file_path).split('_preserved')[0]
    channel_name_clean = channel_name.strip().replace(" ", "_").lower()
    os.makedirs(results_folder, exist_ok=True)

    # График
    fig, ax = plt.subplots(figsize=(8, 6))
    xs = ['negative', 'neutral', 'positive']
    ys = [label_counts[x] for x in xs]
    ax.bar(xs, ys, color=['red', 'gray', 'green'])
    ax.set_title('Распределение меток сентимента')
    ax.set_xlabel('Метка сентимента')
    ax.set_ylabel('Количество предложений')
    for i, freq in enumerate(ys):
        ax.text(i, freq, str(freq), ha='center', va='bottom')
    sentiment_plot_path = os.path.join(results_folder, f"{channel_name_clean}_sentiment_plot.png")
    plt.tight_layout()
    plt.savefig(sentiment_plot_path)
    plt.close(fig)

    return sentiment_plot_path
