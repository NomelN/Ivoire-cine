"""
Routes pour les films
"""
from flask import Blueprint, render_template, request, abort
from app.services.tmdb_service import tmdb_service
from app.utils.validators import validate_page, validate_query, validate_genre_id

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def home():
    """Page d'accueil avec films populaires"""
    page = validate_page(request.args.get('page', 1))

    data, error = tmdb_service.get_popular_movies(page)

    if data:
        movies = data.get("results", [])
        total_pages = data.get("total_pages", 1)
        return render_template(
            "movies_paginated.html",
            movies=movies,
            page=page,
            total_pages=total_pages
        )
    else:
        return render_template(
            "error.html",
            error=error or "Erreur lors de la récupération des films"
        )

@movies_bp.route('/search')
def search():
    """Recherche de films"""
    query = request.args.get('query')
    validated_query = validate_query(query)

    if validated_query:
        data, error = tmdb_service.search_movies(validated_query)

        if data:
            movies = data.get('results', [])
            return render_template(
                'search_results.html',
                movies=movies,
                query=validated_query
            )
        else:
            return render_template(
                "error.html",
                error=error or "Erreur lors de la recherche"
            )
    else:
        return render_template(
            "search_results.html",
            movies=[],
            query=query or ""
        )

@movies_bp.route('/genre/<int:genre_id>')
def movies_by_genre(genre_id):
    """Films filtrés par genre"""
    validated_genre_id = validate_genre_id(genre_id)
    if not validated_genre_id:
        abort(404)

    page = validate_page(request.args.get('page', 1))

    # Récupérer les films du genre
    data, error = tmdb_service.discover_movies_by_genre(validated_genre_id, page)

    # Récupérer le nom du genre
    genres_data, _ = tmdb_service.get_genres()
    genres_dict = {}
    if genres_data:
        genres_dict = {
            genre['id']: genre['name']
            for genre in genres_data.get('genres', [])
        }

    genre_name = genres_dict.get(validated_genre_id, "Inconnu")

    if data:
        movies = data.get("results", [])
        total_pages = data.get("total_pages", 1)
        return render_template(
            "movies_by_genre.html",
            movies=movies,
            genre_id=validated_genre_id,
            genre_name=genre_name,
            total_pages=total_pages,
            page=page
        )
    else:
        return render_template(
            "error.html",
            error=error or f"Erreur lors de la récupération des films pour le genre {genre_name}"
        )

@movies_bp.route('/category/<string:category>')
def movies_by_category(category):
    """Films filtrés par catégorie TMDB"""
    # Mapper les catégories avec les endpoints TMDB
    category_map = {
        "now_playing": "Films en Salle",
        "popular": "Films Populaires",
        "top_rated": "Films les Mieux Notés",
        "upcoming": "Films à Venir"
    }

    if category not in category_map:
        abort(404)

    page = validate_page(request.args.get('page', 1))

    # Utiliser le service TMDB pour les catégories
    if category == 'popular':
        data, error = tmdb_service.get_popular_movies(page)
    else:
        # Pour les autres catégories, faire un appel direct via le service
        from app.services.tmdb_service import tmdb_service as service
        endpoint = f"movie/{category}"
        data, error = service._make_request(endpoint, {"page": page})

    category_name = category_map[category]

    if data:
        movies = data.get("results", [])
        total_pages = min(data.get("total_pages", 1), 500)
        return render_template(
            "movies_by_category.html",
            movies=movies,
            category=category,
            category_name=category_name,
            total_pages=total_pages,
            page=page
        )
    else:
        return render_template(
            "error.html",
            error=error or f"Erreur lors de la récupération des films pour la catégorie {category_name}"
        )