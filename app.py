import streamlit as st
import pickle
import requests
st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=5bf593a90ea62a983312181c5e5ca44a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
         movie_id = movies.iloc[i[0]].id
         recommended_movie_posters.append(fetch_poster(movie_id))
         recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

cols = st.columns(5)
if st.button('Recommand'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
# Loop through each movie and poster, and display them in columns
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_column_width=True)
            st.write(recommended_movie_names[i])

        
