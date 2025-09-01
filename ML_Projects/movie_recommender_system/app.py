import streamlit as st
import pickle
import requests



@st.cache_data
def load_df():
    with open("movie.pkl", "rb") as f:
        return pickle.load(f)
df= load_df()
similarity = pickle.load(open("similarity.pkl", "rb"))

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZmU5M2E3M2Q5MWQ4YTE0ZWI4YTQ5NGI0ODk0YjY4ZSIsIm5iZiI6MTc1NjMwNTcyMC45NjQsInN1YiI6IjY4YWYxOTM4Njk0MmYxN2E5YjNkOGI1OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Hu1mDzZ7a-4P20XzqLAYHQIJVnwdLbcKs8ehs4TBk3M"
}

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}language=en-US".format(movie_id), headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_df = df[df['title'] == movie].index[0]
    distances = similarity[movie_df]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = df.iloc[i[0], 0]
        recommended_movies.append(df.iloc[i[0]][1])
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


st.title('Movie Recommender')
movie_selection = st.selectbox(
    "Choose a Movie",
    df['title'].values

)

if st.button('Recommend'):
    st.markdown(f"### 🎬 **You have Selected: {movie_selection}**")
    name, posters = recommend(movie_selection)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{name[0]}</p>",
            unsafe_allow_html=True
        )
        st.image(posters[0], use_container_width=True)
    with col2:
        st.markdown(
            f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{name[1]}</p>",
            unsafe_allow_html=True
        )
        st.image(posters[1], use_container_width=True)
    with col3:
        st.markdown(
            f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{name[2]}</p>",
            unsafe_allow_html=True
        )
        st.image(posters[2], use_container_width=True)
    with col4:
        st.markdown(
            f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{name[3]}</p>",
            unsafe_allow_html=True
        )
        st.image(posters[3], use_container_width=True)
    with col5:
        st.markdown(
            f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{name[4]}</p>",
            unsafe_allow_html=True
        )
        st.image(posters[4], use_container_width=True)