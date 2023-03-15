import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

def get_mentions_count(content, phrase):
    lower_content = content.lower()
    lower_phrase = phrase.lower()
    return lower_content.count(lower_phrase)

# Input source URL
source_url = input("Enter source URL: ")
source_page = requests.get(source_url)
source_content = source_page.text

# Get the word count of source URL
source_word_count = len(source_content.split())
print(f"Source URL word count: {source_word_count}")

# Input search phrase
phrase = input("Enter a phrase to search for: ")

# Get count of mentions of the phrase in source URL
source_mentions = get_mentions_count(source_content, phrase)
print(f"Number of mentions in source URL: {source_mentions}")

# Input target URLs
target_urls = [input("Enter target URL: ") for i in range(3)]

# Get count of mentions of the phrase in target URLs
for url in target_urls:
    target_page = requests.get(url)
    target_content = target_page.text

    # Get the word count of target URL
    target_word_count = len(target_content.split())
    print(f"Target URL word count: {target_word_count}")

    target_mentions = get_mentions_count(target_content, phrase)
    print(f"Number of mentions in target URL: {target_mentions}")

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
