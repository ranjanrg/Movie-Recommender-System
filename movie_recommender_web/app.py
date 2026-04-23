from pathlib import Path

from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / 'movies.pkl', 'rb') as movies_file:
    movies = pickle.load(movies_file)

with open(BASE_DIR / 'similarity.pkl', 'rb') as similarity_file:
    similarity = pickle.load(similarity_file)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    selected_movie = ''

    if request.method == 'POST':
        selected_movie = request.form.get('movie', '')
        if selected_movie:
            recommendations = recommend(selected_movie)

    movie_list = movies['title'].values

    return render_template(
        'index.html',
        movie_list=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )


if __name__ == '__main__':
    app.run(debug=True)
