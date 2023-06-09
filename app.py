import requests
from bs4 import BeautifulSoup
from collections import Counter
import streamlit as st
def get_product_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = soup.find_all('span', {'class': 'a-size-base review-text'})
    return [review.get_text() for review in reviews]

def count_words(reviews):
    words = ' '.join(reviews).lower().split()
    word_count = Counter(words)
    return word_count.most_common(3)

def main():
    st.title("Amazon Ürün İnceleme Analizi")
    url = st.text_input("Ürün Linki:")
    rating_threshold = st.slider("Kaç puan altındaki yorumları incelemek istersiniz?", min_value=1, max_value=5, step=1)
    if url:
        reviews = get_product_reviews(url)
        filtered_reviews = [review for review in reviews if float(review.split()[0]) <= rating_threshold]
        st.subheader("En Çok Geçen 3 Kelime:")
        if filtered_reviews:
            word_count = count_words(filtered_reviews)
            for word, count in word_count:
                st.write(f"{word}: {count}")
        else:
            st.write("Filtrelenmiş yorum bulunamadı.")

if __name__ == "__main__":
    main()


