from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from collections import Counter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    url = request.form['url']
    rating_threshold = float(request.form['rating_threshold'])
    reviews = get_product_reviews(url)
    filtered_reviews = [review for review in reviews if float(review.split()[0]) <= rating_threshold]
    word_count = count_words(filtered_reviews)
    return render_template('result.html', word_count=word_count)

def get_product_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = soup.find_all('span', {'class': 'a-size-base review-text'})
    return [review.get_text() for review in reviews]

def preprocess_text(text):
    # Küçük harfe dönüştürme
    text = text.lower()

    # Sayıları ve noktalama işaretlerini silme
    text = text.translate(str.maketrans('', '', string.digits + string.punctuation))

    # Lemmatizasyon
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    # Stopwords kaldırma
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in lemmatized_words if word not in stop_words]

    return filtered_words

def count_words(reviews):
    words = ' '.join(reviews).lower().split()
    word_count = Counter(words)
    return word_count.most_common(3)

if __name__ == '__main__':
    app.run(debug=True)
