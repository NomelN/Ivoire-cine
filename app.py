from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

@app.route('/')
def home():
    # Récupérer le numéro de page depuis l'URL (par défaut : page 1)
    page = request.args.get('page', 1, type=int)

    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "fr-FR",
        "page": page
        }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movies = response.json()["results"]
        total_pages = response.json()["total_pages"]
        return render_template("movies_paginated.html", movies=movies, page=page, total_pages=total_pages)
    else:
        return f"Erreur lors de la récupération des films: {response.status_code}"
    
@app.route('/about')
def about():
    return """
    <h1>À propos</h1>
    <p>Ceci est une application de démonstration utilisant l'API TMDb.</p>
    <a href="/">Retour à l'accueil</a>
    """

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": API_KEY,
            "language": "fr-FR",
            "query":query
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            movies = response.json()['results']
            return render_template('search_results.html', movies=movies, query=query)
        else:
            return f"Erreur lors de la recherche: {response.status_code}"
    else:
        return render_template("search_results.html", movies=[], query=query)

@app.context_processor
def inject_genres():
    """Récupère les genres de films et les injecte dans tous les templates."""
    url = f"{BASE_URL}/genre/movie/list"
    params = {
        "api_key": API_KEY, 
        "language": "fr-FR"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        genres = response.json().get("genres", [])
        genres_dict = {genre['id']: genre['name'] for genre in genres}  # Dictionnaire {id: nom}
        return {"genres": genres, "genres_dict": genres_dict}
    else:
        return {"genres": [], "genres_dict": {}}


@app.route('/genre/<int:genre_id>')
def movies_by_genre(genre_id):
    page = request.args.get('page', 1, type=int)
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "fr-FR",
        "with_genres": genre_id,
        "page": page
    }
    response = requests.get(url, params=params)

    # Récupérer le nom du genre depuis genres_dict
    genre_name = None
    genres_dict = inject_genres().get("genres_dict", {})
    if genre_id in genres_dict:
        genre_name = genres_dict[genre_id]
    else:
        genre_name = "Inconnu"

    if response.status_code == 200:
        movies = response.json().get("results", [])
        total_pages = response.json().get("total_pages", 1)
        return render_template(
            "movies_by_genre.html",
            movies=movies,
            genre_id=genre_id,
            genre_name=genre_name,  # Passer le nom du genre au template
            total_pages=total_pages,
            page=page
        )
    else:
        return f"Erreur lors de la récupération des films pour le genre {genre_id}"
    
if __name__== '__main__':
    app.run(debug=True)