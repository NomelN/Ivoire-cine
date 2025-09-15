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

@movies_bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Page de détail d'un film"""
    # Valider l'ID du film
    if movie_id <= 0:
        abort(404)

    # Récupérer les détails du film
    movie_data, error = tmdb_service.get_movie_details(movie_id)

    if not movie_data:
        return render_template(
            "error.html",
            error=error or "Film non trouvé"
        )

    # Extraire les données utiles
    movie = movie_data
    cast = movie_data.get('credits', {}).get('cast', [])[:10]  # Top 10 acteurs
    crew = movie_data.get('credits', {}).get('crew', [])
    similar_movies = movie_data.get('similar', {}).get('results', [])[:6]
    videos = movie_data.get('videos', {}).get('results', [])

    # Filtrer les vidéos pour ne garder que les trailers YouTube
    trailers = [
        video for video in videos
        if video.get('type') == 'Trailer' and video.get('site') == 'YouTube'
    ][:3]

    # Trouver le réalisateur
    director = None
    for person in crew:
        if person.get('job') == 'Director':
            director = person.get('name')
            break

    return render_template(
        "movie_detail.html",
        movie=movie,
        cast=cast,
        director=director,
        similar_movies=similar_movies,
        trailers=trailers
    )

@movies_bp.route('/advanced-search')
def advanced_search():
    """Recherche avancée avec filtres"""
    # Récupérer les genres pour le formulaire
    genres_data, _ = tmdb_service.get_genres()
    genres = genres_data.get('genres', []) if genres_data else []

    # Récupérer les paramètres de recherche
    query = request.args.get('query', '').strip()
    genre_id = request.args.get('genre_id', type=int)
    year = request.args.get('year', type=int)
    min_rating = request.args.get('min_rating', type=float)
    sort_by = request.args.get('sort_by', 'popularity.desc')
    page = validate_page(request.args.get('page', 1))

    movies = []
    total_pages = 1
    error = None

    # Si des filtres sont appliqués
    if any([query, genre_id, year, min_rating]):
        # Construire les paramètres de recherche
        params = {
            'page': page,
            'sort_by': sort_by,
            'vote_count.gte': 10  # Films avec au moins 10 votes
        }

        # Ajouter les filtres
        if genre_id:
            params['with_genres'] = genre_id

        if year:
            params['primary_release_year'] = year

        if min_rating:
            params['vote_average.gte'] = min_rating

        if query:
            # Si une requête textuelle est présente, utiliser l'endpoint de recherche
            validated_query = validate_query(query)
            if validated_query:
                data, error = tmdb_service.search_movies(validated_query, page)
                if data:
                    # Filtrer les résultats selon les critères additionnels
                    movies = data.get('results', [])
                    if genre_id or min_rating or year:
                        movies = filter_search_results(movies, genre_id, min_rating, year)
                    total_pages = data.get('total_pages', 1)
        else:
            # Utiliser l'endpoint discover
            data, error = tmdb_service._make_request('discover/movie', params)
            if data:
                movies = data.get('results', [])
                total_pages = min(data.get('total_pages', 1), 500)

    return render_template(
        'advanced_search.html',
        movies=movies,
        genres=genres,
        query=query,
        selected_genre_id=genre_id,
        selected_year=year,
        selected_min_rating=min_rating,
        selected_sort_by=sort_by,
        page=page,
        total_pages=total_pages,
        error=error
    )


def filter_search_results(movies, genre_id=None, min_rating=None, year=None):
    """Filtre les résultats de recherche selon des critères additionnels"""
    filtered_movies = []

    for movie in movies:
        # Filtrer par genre
        if genre_id and genre_id not in movie.get('genre_ids', []):
            continue

        # Filtrer par note minimale
        if min_rating and movie.get('vote_average', 0) < min_rating:
            continue

        # Filtrer par année
        if year and movie.get('release_date'):
            movie_year = int(movie['release_date'][:4])
            if movie_year != year:
                continue

        filtered_movies.append(movie)

    return filtered_movies