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


if __name__== '__main__':
    app.run(debug=True)