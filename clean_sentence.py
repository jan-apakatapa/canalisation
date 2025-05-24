import json
import re
import os
from unidecode import unidecode

def process_clear_sentence(file_path, results_folder):
    """Функция для очистки и обработки текста из файла.
    Сохраняет очищенный текст в файл и возвращает путь к нему.
    """
    # Загружаем данные
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Получаем имя канала
    channel_name = data.get("name", "channel")
    channel_name_clean = re.sub(r'[^\w\s]', '', channel_name)
    channel_name_clean = unidecode(channel_name_clean).strip().replace(" ", "_").lower()

    # Обработка текста
    sentences = []
    for msg in data.get("messages", []):
        text_parts = []
        if isinstance(msg.get("text"), str):
            text_parts.append(msg["text"])
        elif isinstance(msg.get("text"), list):
            for part in msg["text"]:
                if isinstance(part, str):
                    text_parts.append(part)
                elif isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])
        combined_text = ' '.join(text_parts).strip()

        # Добавим точку, если нет в конце знака окончания
        if combined_text and not re.search(r'[.!?…]$', combined_text):
            combined_text += '.'

        # Очищаем лишнее
        combined_text = re.sub(r'\s+', ' ', combined_text)
        combined_text = re.sub(r'\s([?.!,:;])', r'\1', combined_text)
        combined_text = re.sub(r'[^\w\s.,?!:;\'\"()-]', '', combined_text)
        sentences.append(combined_text.strip())

    # Объединяем все в один текст
    clean_text = ' '.join(sentences)

    # Сохраняем очищенный текст в файл
    output_filename = f"{channel_name_clean}_clean_sentence.txt"
    output_path = os.path.join(results_folder, output_filename)
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(clean_text)

    # Возвращаем путь к файлу с очищенным текстом
    return output_path
