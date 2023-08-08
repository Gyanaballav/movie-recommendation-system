import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c3d2de4761411e1ebc42c0a3ecb50c46&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/original/"+data['poster_path']
    #return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
     
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    rec_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in rec_movies_list:
        #movie_id = i[0]
        movie_id = movies_list.iloc[i[0]].movie_id
        #fetch poster from API

        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

st.title('Movie Recommender System')

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = pd.DataFrame(movies_list, columns=['title'])
#movie_id = pd.DataFrame(movies_list, columns=['id'])
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox('Select the movie', movies_list['title'])

if st.button('Recommend'):
    recommendations,poster = recommend(selected_movie_name)
    if len(recommendations) == 0:
        st.write('No recommendations found.')
    else:
        st.write('Recommended Movies:')
        # for i, movie in enumerate(recommendations):
        #     st.write(f'{i + 1}. {movie}')
        col1, col2, col3, col4, col5 = st.beta_columns(5)
        with col1:
            st.text(recommendations[0])
            st.image(poster[0])
        with col2:
            st.text(recommendations[1])
            st.image(poster[1])

        with col3:
            st.text(recommendations[2])
            st.image(poster[2])
        with col4:
            st.text(recommendations[3])
            st.image(poster[3])
        with col5:
            st.text(recommendations[4])
            st.image(poster[4])
