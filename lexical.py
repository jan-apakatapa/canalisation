import nltk
import textstat
from lexicalrichness import LexicalRichness
import os

nltk.download('punkt')

class LexicalAnalyzer:
    def __init__(self, text):
        self.text = text
        self.lex = LexicalRichness(text)

    def perform_lexical_analysis(self):
        report = f"""
        🧠 ЛЕКСИЧЕСКИЙ АНАЛИЗ:
        Общее число слов: {self.lex.words}
        Уникальных слов (types): {self.lex.terms}
        Type-Token Ratio (TTR): {self.lex.ttr:.2f}
        MTLD: {self.lex.mtld():.2f}
        HD-D: {self.lex.hdd():.2f}

        📚 ЧИТАЕМОСТЬ:
        Flesch-Kincaid Grade Level: {textstat.flesch_kincaid_grade(self.text):.2f}
        Flesch Reading Ease Score: {textstat.flesch_reading_ease(self.text):.2f}
        Длина предложения в среднем: {textstat.avg_sentence_length(self.text):.2f} слов
        Средняя длина слова: {textstat.avg_letter_per_word(self.text):.2f} букв
        """
        return report

    def save_report(self, results_folder, channel_name_clean):
        report = self.perform_lexical_analysis()
        lexical_report_path = os.path.join(results_folder, f"{channel_name_clean}_lexical_report.txt")
        with open(lexical_report_path, 'w', encoding='utf-8') as out:
            out.write(report)
        return lexical_report_path

if __name__ == '__main__':
    text = "Текст, который вы хотите проанализировать."
    channel_name_clean = "example_channel"
    results_folder = os.path.join('results', channel_name_clean)
    os.makedirs(results_folder, exist_ok=True)

    analyzer = LexicalAnalyzer(text)
    result_path = analyzer.save_report(results_folder, channel_name_clean)
    print(f"Анализ завершён! Отчёт сохранён как: {result_path}")
