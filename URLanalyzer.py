from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import re
import emoji

app = Flask(__name__)

def count_tags(soup, tags):
    if isinstance(tags, str):
        tags = [tags]
    return sum(len(soup.find_all(tag)) for tag in tags)

def count_words(soup):
    text = soup.get_text()
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_emojis(soup):
    text = soup.get_text()
    return len([c for c in text if c in emoji.UNICODE_EMOJI])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    target_url = request.form['target_url']
    source_url_1 = request.form['source_url_1']
    source_url_2 = request.form['source_url_2']
    source_url_3 = request.form['source_url_3']
    search_kw = request.form['search_kw'].lower()

    # Get page source using Requests library
    target_response = requests.get(target_url)
    source_1_response = requests.get(source_url_1)
    source_2_response = requests.get(source_url_2)
    source_3_response = requests.get(source_url_3)

    # Measure page speed using Requests library
    target_page_speed = target_response.elapsed.total_seconds() * 1000
    source_1_page_speed = source_1_response.elapsed.total_seconds() * 1000
    source_2_page_speed = source_2_response.elapsed.total_seconds() * 1000
    source_3_page_speed = source_3_response.elapsed.total_seconds() * 1000

    # Parse HTML content using BeautifulSoup
    target_soup = BeautifulSoup(target_response.content, 'html.parser')
    source_1_soup = BeautifulSoup(source_1_response.content, 'html.parser')
    source_2_soup = BeautifulSoup(source_2_response.content, 'html.parser')
    source_3_soup = BeautifulSoup(source_3_response.content, 'html.parser')

    # Count tags, words, and emojis for each page
    target_img_count = count_tags(target_soup, 'img')
    target_link_count = count_tags(target_soup, 'a')
    target_word_count = count_words(target_soup)
    target_header_count = count_tags(target_soup, ['h1', 'h2', 'h3', 'h4'])
    target_emoji_count = count_emojis(target_soup)

    source_1_img_count = count_tags(source_1_soup, 'img')
    source_1_link_count = count_tags(source_1_soup, 'a')
    source_1_word_count = count_words(source_1_soup)
    source_1_header_count = count_tags(source_1_soup, ['h1', 'h2', 'h3', 'h4'])
    source_1_emoji_count = count_emojis(source_1_soup)

    source_2_img_count = count_tags(source_2_soup, 'img')
    source_2_link_count = count_tags(source_2_soup, 'a')
    source_2_word_count = count_words(source_2_soup)
    source_2_header_count = count_tags(source_2_soup, ['h1', 'h2', 'h3', 'h4'])
    source_2_emoji_count = count_emojis(source_2_soup)

    source_3_img_count = count_tags(source_3_soup, 'img')
    source_3_link_count = count_tags(source_3_soup, 'a')
    source_3_word_count = count_words(source_3_soup)
    source_3_header_count = count_tags(source_3_soup, ['h1', 'h2', 'h3', 'h4'])
    source_3_emoji_count = count_emojis(source_3_soup)

    # Render result.html template and pass in variables
    return render_template('result.html', target_url=target_url, source_url_1=source_url_1,
                           source_url_2=source_url_2, source_url_3=source_url_3, search_kw=search_kw,
                           target_img_count=target_img_count, target_link_count=target_link_count,
                           target_word_count=target_word_count, target_header_count=target_header_count,
                           target_emoji_count=target_emoji_count, source_1_img_count=source_1_img_count,
                           source_1_link_count=source_1_link_count, source_1_word_count=source_1_word_count,
                           source_1_header_count=source_1_header_count, source_1_emoji_count=source_1_emoji_count,
                           source_2_img_count=source_2_img_count, source_2_link_count=source_2_link_count,
                           source_2_word_count=source_2_word_count, source_2_header_count=source_2_header_count,
                           source_2_emoji_count=source_2_emoji_count, source_3_img_count=source_3_img_count,
                           source_3_link_count=source_3_link_count, source_3_word_count=source_3_word_count,
                           source_3_header_count=source_3_header_count, source_3_emoji_count=source_3_emoji_count,
                           target_page_speed=target_page_speed, source_1_page_speed=source_1_page_speed,
                           source_2_page_speed=source_2_page_speed, source_3_page_speed=source_3_page_speed)

if __name__ == '__main__':
    app.run(debug=True)
