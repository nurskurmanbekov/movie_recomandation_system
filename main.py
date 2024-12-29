import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Загрузка данных
@st.cache
def load_data():
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    credits.columns = ['id', 'title', 'cast', 'crew']
    movies = movies.merge(credits, on='id')
    return movies

movies = load_data()

# Заголовок приложения
st.title("Movie Recommendation System")
st.write("Выберите тип системы рекомендаций:")

# Выбор метода
method = st.selectbox("Метод рекомендаций", ["Демографический", "На основе контента"])

# Демографический фильтр
if method == "Демографический":
    st.subheader("Топ фильмов по популярности")
    num_movies = st.slider("Количество фильмов", 1, 20, 10)
    top_movies = movies.sort_values("popularity", ascending=False).head(num_movies)
    st.write(top_movies[["title", "popularity"]])

# Рекомендации на основе контента
elif method == "На основе контента":
    st.subheader("Рекомендации на основе описания сюжета")
    tfidf = TfidfVectorizer(stop_words="english")
    movies["overview"] = movies["overview"].fillna("")
    tfidf_matrix = tfidf.fit_transform(movies["overview"])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(movies.index, index=movies["title"]).drop_duplicates()

    def get_recommendations(title, cosine_sim=cosine_sim):
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]
        return movies["title"].iloc[movie_indices]

    movie_title = st.text_input("Введите название фильма", "The Dark Knight Rises")
    if st.button("Показать рекомендации"):
        recommendations = get_recommendations(movie_title)
        st.write(recommendations)

# Запуск приложения
st.write("Приложение для демонстрации рекомендаций.")
