from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.digits + string.punctuation))
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in lemmatized_words if word not in stop_words]
    return filtered_words

def get_product_reviews(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = soup.find_all('span', {'class': 'a-size-base review-text'})
    return [review.get_text() for review in reviews]

def count_words(reviews):
    words = [preprocess_text(review) for review in reviews if review.strip()]
    words = [word for sublist in words for word in sublist]
    word_count = Counter(words)
    return word_count.most_common(3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    rating_threshold = integer(request.form['rating_threshold'])
    reviews = get_product_reviews(url)
    filtered_reviews = [review for review in reviews if review.strip() and integer(review.split()[0]) <= rating_threshold]
    word_count = count_words(filtered_reviews)
    return render_template('result.html', word_count=word_count)

if __name__ == "__main__":
    app.run(debug=False)

