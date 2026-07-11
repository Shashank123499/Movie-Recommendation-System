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

        recommendations.append(
            {
                "title": movie_title,
                "genre": movie_genre
            }
        )

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

                st.markdown(f"### {i}. {m['title']}")

                st.write(f"**Genre:** {m['genre']}")

                st.divider()
