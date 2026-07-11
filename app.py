import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# --------------------------
# Load Dataset
# --------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    rating = pd.read_csv(r"C:\Users\Saksham Awasthi\Downloads\ratings.csv")

avg_rating = (
    rating.groupby("movieId")["rating"].mean().reset_index()
)

avg_rating.rename(columns = {"rating": "Average_Rating"},inplace = True)

dataset = dataset.merge(
    avg_rating , on = "movieId",how = "left"
)

df["genres"] = df["genres"].fillna("")
df["genres"] = df["genres"].str.replace("|", " ", regex=False)
df["title"] = df["title"].fillna("")
df["title"] = df["title"].str.lower()

    return df

dataset = load_data()

# --------------------------
# Similarity Matrix
# --------------------------

cv = CountVectorizer(stop_words="english")

vectors = cv.fit_transform(dataset["genres"]).toarray()

similarity = cosine_similarity(vectors)


# --------------------------
# Recommendation Function
# --------------------------

def recommend_movies(movie_name):

    movie_name = movie_name.lower()

    if movie_name not in dataset["title"].values:

        close_match = get_close_matches(
            movie_name,
            dataset["title"].tolist(),
            n=5,
            cutoff=0.5
        )

        if close_match:
            return None, close_match

        return [], []

    movie_index = dataset[dataset["title"] == movie_name].index[0]

    score = list(enumerate(similarity[movie_index]))

    sorted_score = sorted(score,
                          key=lambda x: x[1],
                          reverse=True)

    recommendations = []

    for movie in sorted_score[1:6]:

        movie_title = dataset.iloc[movie[0]]["title"].title()

        movie_genre = dataset.iloc[movie[0]]["genres"]

        movie_rating = dataset.iloc[movie[0]]["Average_Rating"]

       recommendations.append({
             "title": movie_title,
             "genre":movie_genre,
             "rating":round(movie_rating,1)
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

                st.markdown(f"### 🎬 {movie['title']}")

                st.write(f"⭐ Rating: {movie['rating']}/5")

                st.write(f"🎭 Genre: {movie['genre']}")

                st.divider()
