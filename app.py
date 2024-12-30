import streamlit as st
import pickle
import pandas as pd
import requests

# Загружаем данные
movie_list = pickle.load(open("movie_dict.pkl", 'rb'))
movies = pd.DataFrame(movie_list)
movie_title = movies['title'].values
movie_similarity = pickle.load(open("movie_similarity.pkl", 'rb'))

# Функция для получения постера фильма
def fetch_poster(movie_id):
    api_key = "c8f5faba141518d14d23ed2222d3f52a"  # Используем предоставленный ключ API
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    else:
        return "https://via.placeholder.com/500x750?text=Error"

# Функция для получения рекомендованных фильмов
def movie_suggestion(movie_name):
    if movie_name not in movies['title'].values:
        return [], []

    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = movie_similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    suggested_movies = []
    suggested_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        suggested_movie_posters.append(fetch_poster(movie_id))
        suggested_movies.append(movies.iloc[i[0]].title)

    return suggested_movies, suggested_movie_posters

# Интерфейс Streamlit
st.title('Movie Suggestion System')

st.markdown(
    """### Final Project by Kurmanbekov Nursultan  
    Course: Math 21  
    Description: This application is a movie suggestion system developed as part of my final project. 
    It provides personalized movie recommendations based on user input using pre-trained similarity models and The Movie Database (TMDb) API for fetching posters.  
    Enjoy exploring movies!
    """
)

input_movie_title = st.selectbox("Type a movie title to get similar movie suggestions", movie_title)

if st.button('Suggest'):
    suggested_movies, suggested_movie_posters = movie_suggestion(input_movie_title)
    if not suggested_movies:
        st.error("Movie not found. Please try another title.")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(suggested_movie_posters[0])
            st.text(suggested_movies[0])
        with col2:
            st.image(suggested_movie_posters[1])
            st.text(suggested_movies[1])
        with col3:
            st.image(suggested_movie_posters[2])
            st.text(suggested_movies[2])
        with col4:
            st.image(suggested_movie_posters[3])
            st.text(suggested_movies[3])
        with col5:
            st.image(suggested_movie_posters[4])
            st.text(suggested_movies[4])

st.write('This system is developed by _Kurmanbekov Nursultan_')
