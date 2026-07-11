# Movie-Recommendation-System
A content based movie recommendation system system built.

# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using *Python, **Pandas, **Scikit-learn, and **Streamlit*. The application recommends movies based on genre similarity using the CountVectorizer and Cosine Similarity algorithms.

---

## 📌 Features

- Search for a movie by title<br>
- Get the Top 5 similar movie recommendations<br>
- Handles incorrect movie names using close matching<br>
- Displays movie genres<br>
- Fast and lightweight Streamlit interface<br>

---

## 🛠️ Technologies Used

- Python<br>
- Pandas<br>
- Scikit-learn<br>
- Streamlit<br>
- CountVectorizer<br>
- Cosine Similarity<br>
- Difflib<br>

---

## 📂 Dataset

The project uses a dataset containing:

- Movie Title<br>
- Genres

Example:

| Title | Genres |
|-------|---------|
| Toy Story (1995) | Adventure Animation Children Comedy Fantasy |<br>
| Jumanji (1995) | Adventure Children Fantasy |

---

## 🚀 How It Works

1. Load the movie dataset.<br>
2. Clean the genre information.<br>
3. Convert genres into numerical vectors using CountVectorizer.<br>
4. Compute Cosine Similarity between all movies.<br>
5. Search for the user's movie.<br>
6. Recommend the five most similar movies.<br>

---

## 📁 Project Structure


Movie_Recommendation_System/
│
├── app.py<br>
├── movies.csv<br>
├── requirements.txt<br>
├── README.md<br>


---

## ▶️ Installation

Clone the repository

bash<br>
git clone https://github.com/your-username/Movie-Recommendation-System.git


Move into the project directory

bash<br>
cd Movie-Recommendation-System


Install dependencies

bash<br>
pip install -r requirements.txt


Run the application

bash<br>
streamlit run app.py


---

## 📷 Output

The application allows users to:

- Enter a movie title<br>
- Click the *Recommend* button<br>
- View the Top 5 recommended movies along with their genres<br>

---

## 🎯 Future Improvements

- Add movie posters using TMDb API<br>
- Display IMDb ratings<br>
- Show release year<br>
- Recommend based on multiple features (genres, cast, keywords)<br>
- Deploy with Docker<br>
- Improve UI with a Netflix-inspired design

---

## 👨‍💻 Author

*Shashank Awasthi*

- BCA Student<br>
- AI & Machine Learning Enthusiast<br>
- Passionate about Machine Learning, Data Science, and Python Development<br>

---

## ⭐ If you like this project

Give this repository a ⭐ on GitHub if you found it useful.
