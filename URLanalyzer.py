import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

def get_mentions_count(content, phrase):
    lower_content = content.lower()
    lower_phrase = phrase.lower()
    return lower_content.count(lower_phrase)

def analyze_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.body.get_text(' ', strip=True)
    word_count = len(body.split())
    image_count = len(soup.body.find_all('img'))
    link_count = len(soup.body.find_all('a'))
    if link_count > 0:
        link_density = image_count / link_count
    else:
        link_density = 0
    words = body.lower().split()
    return body, word_count, image_count, words, link_density

# ...

@app.route('/result', methods=['POST'])
def result():
    source_url = request.form['source_url']
    phrase = request.form['phrase']
    target_urls = [
        request.form['target_url_1'],
        request.form['target_url_2'],
        request.form['target_url_3'],
    ]

    source_body, source_word_count, source_image_count, source_words, source_link_density = analyze_page(source_url)
    source_mentions = get_mentions_count(source_body, phrase)

    target_results = []
    target_words_list = []
    for url in target_urls:
        target_body, target_word_count, target_image_count, target_words, target_link_density = analyze_page(url)
        target_mentions = get_mentions_count(target_body, phrase)
        target_results.append((url, target_word_count, target_mentions, target_image_count, target_link_density))
        target_words_list.append(target_words)

    common_words = set(target_words_list[0]) & set(target_words_list[1]) & set(target_words_list[2]) - set(source_words)
    words_to_remove = ["the", "of", "and", "a", "to", "in", "is", "you", "that", "he", "was", "for", "on", "are", "as", "with", "his", "they", "i", "at", "there", "some", "my", "of", "be", "this", "have", "each", "which", "she", "do", "how", "their", "if", "will", "up", "other", "about", "out", "many", "then", "them", "these", "so", "some", "her", "would", "make", "like", "him", "into", "time", "has", "look", "two", "more", "write", "go", "see", "number", "no", "way", "could", "people", "my", "than", "first", "water", "been", "call", "who", "oil", "its", "now", "find", "long", "down", "day", "did", "get", "come", "made", "may", "part"]
    common_words = [word for word in common_words if word not in words_to_remove]

    return render_template('result.html', source_url=source_url, source_mentions=source_mentions, phrase=phrase, target_results=target_results, common_words=common_words)

if __name__ == '__main__':
    app.run()
