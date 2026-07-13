import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# --------------------------
# Load Dataset
# --------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    rating = pd.read_csv("ratings.csv")

    avg_rating = (
     rating.groupby("movieId")["rating"].mean().reset_index()
)

    avg_rating.rename(columns = {"rating": "Average_Rating"},inplace = True)

    df = df.merge(
    avg_rating , on = "movieId",how = "left"
)

    df["genres"] = df["genres"].fillna("")
    df["genres"] = df["genres"].str.replace("|", " ", regex=False)
    df["title"] = df["title"].fillna("")
    df["title"] = df["title"].str.lower()

    return df

df = load_data()

# --------------------------
# Similarity Matrix
# --------------------------

cv = CountVectorizer(stop_words="english")

vectors = cv.fit_transform(df["genres"]).toarray()

similarity = cosine_similarity(vectors)

# --------------------------
# Fetch Posters
# --------------------------

API_KEY = "50ef24c3911ab6a7669fe5b809e8eae6"

def fetch_poster(movie_name):

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={quote(movie_name)}"

    response = requests.get(url)
    data = response.json()

    if data.get("results"):

        poster_path = data["results"][0].get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    return None

# --------------------------
# Recommendation Function
# --------------------------

def recommend_movies(movie_name):

    movie_name = movie_name.lower()

    if movie_name not in df["title"].values:

        close_match = get_close_matches(
            movie_name,
            df["title"].tolist(),
            n=5,
            cutoff=0.5
        )

        if close_match:
            return None, close_match

        return [], []

    movie_index = df[df["title"] == movie_name].index[0]

    score = list(enumerate(similarity[movie_index]))

    sorted_score = sorted(score,
                          key=lambda x: x[1],
                          reverse=True)

    recommendations = []

    for movie in sorted_score[1:6]:

        movie_title = df.iloc[movie[0]]["title"].title()

        search_title = movie_title.split("(")[0].strip()

        movie_genre = df.iloc[movie[0]]["genres"]

        movie_rating = df.iloc[movie[0]]["Average_Rating"]

        recommendations.append({
             "title": movie_title,
             "genre":movie_genre,
             "rating":round(movie_rating,1),
             "poster":fetch_poster(search_title)
             })

    return recommendations, []


# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommendation System")

st.write("Enter a movie name and get similar movie recommendations.")

movie = st.text_input("Movie Name")

if st.button("Recommend"):

    if movie == "":
        st.warning("Please enter a movie name.")

    else:

        result, suggestion = recommend_movies(movie)

        if result is None:

            st.error("Movie not found.")

            st.write("Did you mean:")

            for s in suggestion:
                st.write("•", s.title())

        else:

            st.success("Top 5 Recommendations")

            for i, m in enumerate(result, 1):

                if m["poster"] :
                 
                 st.image(m["poster"], width=180)

                else:
                    st.write("🖼️ Poster not available")

                st.markdown(f"### 🎬 {m['title']}")

                st.write(f"⭐ Rating: {m['rating']}/5")

                st.write(f"🎭 Genre: {m['genre']}")

                st.divider()
