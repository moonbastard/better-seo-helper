import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

def get_mentions_count(content, phrase):
    lower_content = content.lower()
    lower_phrase = phrase.lower()
    return lower_content.count(lower_phrase)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    source_url = request.form['source_url']
    phrase = request.form['phrase']
    target_urls = [
        request.form['target_url_1'],
        request.form['target_url_2'],
        request.form['target_url_3'],
    ]

    source_page = requests.get(source_url)
    source_content = source_page.text
    source_word_count = len(source_content.split())
    source_mentions = get_mentions_count(source_content, phrase)

    target_results = []
    for url in target_urls:
        target_page = requests.get(url)
        target_content = target_page.text
        target_word_count = len(target_content.split())
        target_mentions = get_mentions_count(target_content, phrase)
        target_results.append((url, target_word_count, target_mentions))

    return render_template('result.html', source_url=source_url, source
