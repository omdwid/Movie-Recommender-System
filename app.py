import streamlit as st
import pickle
import requests
import pandas as pd

st.title('Movie Recommender System')

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZTcyMjljNmVlNzRhN2JhM2FiZGZmZTExNDZmOGY5NyIsInN1YiI6IjY0ODg1ZjU0ZTI3MjYwMDEyODdiNzIyMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HE4fDOWxPTBrcb8fQFIvy0mbEZknBuzuHC-04V_biJE"
    }
    response = requests.get(url, headers=headers).json()
    poster_path = response['posters'][0]['file_path']
    return poster_path

def recommend(movie):
    movie = movie.lower()
    filt = movies['title'] == movie
    if len(movies.loc[filt]) == 0:
        print("enter a valid name")
        return
    idx = movies[filt].index[0]
    similar = list(enumerate(similarity[idx]))
    sim = sorted(similar, key=lambda x: x[1], reverse=True)

    recommendations = []
    images = []
    for i, s in sim[1:6]:
        id = movies.loc[i, 'movie_id']
        name = movies.loc[i, 'title']
        img_url = 'https://image.tmdb.org/t/p/original' + fetch_poster(id)
        recommendations.append(name)
        images.append(img_url)

    return recommendations, images

option = st.selectbox(
    'Select a movies which you like the most',
    movies['title'].values
)

c1, c2, c3 = st.columns(3, gap="medium")

if c2.button('Recommend'):
    st.subheader(f'Movie you selected: {option}')
    id = movies[movies['title'] == option]['movie_id'].values[0]
    url = 'https://image.tmdb.org/t/p/original'+fetch_poster(id)
    st.image(url, width=150)
    st.divider()
    st.subheader('Top 5 Recommendations')
    recommendations, imgs = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    with col1:
        st.text(recommendations[0])
        st.image(imgs[0])
    with col2:
        st.text(recommendations[1])
        st.image(imgs[1])
    with col3:
        st.text(recommendations[2])
        st.image(imgs[2])
    with col4:
        st.text(recommendations[3])
        st.image(imgs[3])
    with col5:
        st.text(recommendations[4])
        st.image(imgs[4])


# st.write('You selected:', option)
