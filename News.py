from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json
import nltk
from collections import Counter

#Ngonekin ke HTML
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        output = news_extractor(url)
        return render_template('result.html', output=output)
    return render_template('index.html')

#News Extractor
def news_extractor(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    json_data = soup.find('script', type='application/ld+json').get_text()
    location = soup.find('span', class_='source__location').get_text()
    if location == "":
        location = "-"

    data = json.loads(json_data)

    article_body = data.get('articleBody', None)
    article_headline = data.get('headline', None)
    article_date = data.get('dateModified', None)
    article_tag = data.get('articleSection', None)
    article_actor = extract_names(article_body)
    
    output = [article_headline, article_date[:10], article_tag, article_actor, location]
    return output

#Ekstrak nama 
def extract_names(text):
    names = []
    
    for sent in nltk.sent_tokenize(text):
      for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
         if hasattr(chunk, 'label'):
            if chunk.label() == "PERSON":
                names.append(' '.join(c[0] for c in chunk))
    
    # Returning most common name as the most relevant one
    most_common_name = Counter(names).most_common(1)[0][0]
    return most_common_name

