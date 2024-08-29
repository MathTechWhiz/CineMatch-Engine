import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5db7bd7a04063f0e2f15f8ac83ee69d3&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for movie_tuple in movies_list:  # Changed 'i' to 'movie_tuple'
        movie_id = movies.iloc[movie_tuple[0]].movie_id
        recommended_movies.append(movies.iloc[movie_tuple[0]].title)
        # fetch the poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster


# Load the movies DataFrame
movies = pickle.load(open('movies.pkl', 'rb'))

# Extract the list of movie titles
movie_list = movies['title'].values

# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

# selectable for movie selection
selected_movie_name = st.selectbox(
    "Select a movie:",
    movie_list
)

# Recommend button
if st.button("Recommend"):
    name, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])
