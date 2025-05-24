import json
import re
import os
from unidecode import unidecode
import nltk
from nltk.corpus import stopwords
import pymorphy3

# Загрузка стоп-слов
nltk.download('stopwords')
stop_words = set(stopwords.words("russian"))

excluded_words = {
    "это", "всё", "этот", "та", "тот", "там", "когда", "чтобы", "он", "она", "они", "в", "на", "с",
    "и", "не", "за", "по", "под", "был", "бы", "к", "все", "один", "так", "себя", "его", "но", "ли",
    "да", "для", "кто", "что", "или", "меня", "такой", "такое", "как", "поэтому", "этими", "этих", "нам",
    "день", "ещё", "просто", "сегодня", "которые", "почему", "мои", "буду", "типа", "который", "хочу", "всем",
    "моей", "каждый", "пока", "вообще", "зато", "чето", "тебе", "её", "никто", "кстати", "очень", "чтото",
    "могу", "изза", "the", "нужно", "такая", "такие", "люди", "людей", "снова", "делать", "ура"
}

morph = pymorphy3.MorphAnalyzer()

def lemmatize_word(word):
    try:
        parses = morph.parse(word)
        # Если pymorphy не может распознать слово, вернет то же слово
        if parses and parses[0].normal_form:
            return parses[0].normal_form
        else:
            return word
    except Exception:
        return word  # если что-то пошло не так, возвращаем исходное слово

def process_clearwords(file_path, results_folder):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    channel_name = data.get("name", "default_channel")
    channel_name = re.sub(r'[^\w\s]', '', channel_name)
    channel_name = unidecode(channel_name).strip().replace(" ", "_").lower()
    output_filename = f"{channel_name}_clean_words.txt"
    output_path = os.path.join(results_folder, output_filename)

    texts = []
    for message in data.get("messages", []):
        text = message.get("text")
        if isinstance(text, str):
            texts.append(text)
        elif isinstance(text, list):
            for item in text:
                if isinstance(item, str):
                    texts.append(item)
                elif isinstance(item, dict) and "text" in item:
                    texts.append(item["text"])

    full_text = " ".join(texts).lower()
    # Очищаем текст от ссылок, упоминаний, пунктуации и чисел
    cleaned_text = re.sub(r"https?://\S+", "", full_text)
    cleaned_text = re.sub(r"[@#]\w+", "", cleaned_text)
    cleaned_text = re.sub(r"[.,!?…:;—\-]", " ", cleaned_text)
    cleaned_text = re.sub(r"[^\w\sёЁ]", "", cleaned_text)
    cleaned_text = re.sub(r"\d+", "", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    words = cleaned_text.split()

    lemmatized_words = []
    for word in words:
        lemma = lemmatize_word(word)
        if lemma:  # если что-то пошло не так и лемма пустая, не добавляем
            lemmatized_words.append(lemma)
        else:
            lemmatized_words.append(word)

    # Удаляем стоп-слова и excluded_words
    final_words = []
    for word in lemmatized_words:
        if word not in stop_words and word not in excluded_words:
            final_words.append(word)

    final_text = " ".join(final_words)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"Готово! Файл '{output_filename}' создан в папке результатов: {results_folder}")

    return output_path
