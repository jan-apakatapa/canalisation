from flask import Flask, render_template, request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
from clean_words import process_clearwords  # Модуль для CleanWords
from top_words import generate_topwords_plot  # Модуль для графика TopWords
from entities import generate_entities_plot  # Модуль для графика Entities
from clean_sentence import process_clear_sentence  # Модуль для CleanSentence
from lexical import LexicalAnalyzer  # Используем класс вместо функции
from sentiment import perform_sentiment_analysis  # Модуль для сентимент-анализа

app = Flask(__name__)

# Конфигурация для загрузки файлов
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'json'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Главная страница с формой загрузки файла
@app.route('/')
def index():
    return render_template('index.html')

# Страница для обработки файла
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Добавим расширение, если его нет
        if not filename.lower().endswith('.json'):
            filename += '.json'

        # Убедимся, что папка uploads существует
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Проверим, не является ли file_path директорией
        if os.path.isdir(file_path):
            return f'Ошибка: путь {file_path} — это папка, а не файл. Переименуйте файл.'

        # Сохраняем файл
        file.save(file_path)

        # Читаем данные из JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Получаем имя канала из данных
        channel_name = data.get("name", "channel")
        channel_name_clean = channel_name.strip().replace(" ", "_").lower()
        results_folder = os.path.join(app.config['RESULTS_FOLDER'], channel_name_clean)
        os.makedirs(results_folder, exist_ok=True)

        # Запускаем параллельную обработку модулей
        cleaned_text_path = process_clearwords(file_path, results_folder)
        processed_file_path = process_clear_sentence(file_path, results_folder)
        generate_topwords_plot(cleaned_text_path, results_folder)
        generate_entities_plot(cleaned_text_path, results_folder)

        # Проверка, существует ли обработанный файл
        if not os.path.exists(processed_file_path):
            return f"Ошибка: файл {processed_file_path} не найден. Проверьте функцию process_clear_sentence.", 500

        # Новый способ лексического анализа
        with open(processed_file_path, 'r', encoding='utf-8') as f:
            processed_text = f.read()

        analyzer = LexicalAnalyzer(processed_text)
        analyzer.save_report(results_folder, channel_name_clean)

        perform_sentiment_analysis(processed_file_path, results_folder)

        return f'Обработка завершена! Результаты сохранены в папке: {results_folder}'

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
