python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m spacy download ru_core_news_sm
python3 app.py
