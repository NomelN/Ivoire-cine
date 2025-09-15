"""
Service pour l'API TMDB avec cache et gestion d'erreurs
"""
import requests
import time
from typing import Optional, Dict, Any, Tuple
from app.config.settings import get_config

config = get_config()

class TMDBCache:
    """Cache simple en mémoire pour les données TMDB"""
    def __init__(self):
        self._cache = {}
        self._timestamps = {}

    def get(self, key: str) -> Optional[Dict[Any, Any]]:
        """Récupère une valeur du cache si elle n'est pas expirée"""
        if key not in self._cache:
            return None

        if time.time() - self._timestamps[key] > config.CACHE_TIMEOUT:
            # Cache expiré
            del self._cache[key]
            del self._timestamps[key]
            return None

        return self._cache[key]

    def set(self, key: str, value: Dict[Any, Any]) -> None:
        """Ajoute une valeur au cache"""
        self._cache[key] = value
        self._timestamps[key] = time.time()

    def clear(self) -> None:
        """Vide le cache"""
        self._cache.clear()
        self._timestamps.clear()

class TMDBService:
    """Service pour interagir avec l'API TMDB"""

    def __init__(self):
        self.cache = TMDBCache()
        config.validate()  # Valider la configuration au démarrage

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Effectue une requête à l'API TMDB avec gestion d'erreurs

        Returns:
            Tuple[data, error_message]
        """
        # Ajouter la clé API aux paramètres
        params['api_key'] = config.TMDB_API_KEY
        params['language'] = 'fr-FR'

        url = f"{config.TMDB_BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=config.REQUEST_TIMEOUT)

            if response.status_code == 200:
                return response.json(), None
            elif response.status_code == 401:
                return None, "Clé API invalide"
            elif response.status_code == 404:
                return None, "Ressource non trouvée"
            elif response.status_code == 429:
                return None, "Trop de requêtes - veuillez patienter"
            else:
                return None, "Service temporairement indisponible"

        except requests.exceptions.Timeout:
            return None, "Timeout - service trop lent"
        except requests.exceptions.ConnectionError:
            return None, "Erreur de connexion"
        except Exception:
            return None, "Erreur inattendue"

    def get_popular_movies(self, page: int = 1) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """Récupère les films populaires"""
        cache_key = f"popular_movies_page_{page}"

        # Vérifier le cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data, None

        # Faire la requête API
        data, error = self._make_request("movie/popular", {"page": page})

        if data:
            # Limiter le nombre total de pages
            if 'total_pages' in data:
                data['total_pages'] = min(data['total_pages'], 500)

            # Mettre en cache
            self.cache.set(cache_key, data)

        return data, error

    def search_movies(self, query: str, page: int = 1) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """Recherche des films"""
        cache_key = f"search_{query}_{page}"

        # Vérifier le cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data, None

        # Faire la requête API
        data, error = self._make_request("search/movie", {
            "query": query,
            "page": page
        })

        if data:
            # Mettre en cache
            self.cache.set(cache_key, data)

        return data, error

    def get_genres(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """Récupère la liste des genres (mise en cache longue durée)"""
        cache_key = "movie_genres"

        # Vérifier le cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data, None

        # Faire la requête API
        data, error = self._make_request("genre/movie/list", {})

        if data:
            # Mettre en cache avec une durée plus longue pour les genres
            self.cache.set(cache_key, data)

        return data, error

    def discover_movies_by_genre(self, genre_id: int, page: int = 1) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """Découvre des films par genre"""
        cache_key = f"discover_genre_{genre_id}_page_{page}"

        # Vérifier le cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data, None

        # Faire la requête API
        data, error = self._make_request("discover/movie", {
            "with_genres": genre_id,
            "page": page
        })

        if data:
            # Limiter le nombre total de pages
            if 'total_pages' in data:
                data['total_pages'] = min(data['total_pages'], 500)

            # Mettre en cache
            self.cache.set(cache_key, data)

        return data, error

    def get_movie_details(self, movie_id: int) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """Récupère les détails complets d'un film"""
        cache_key = f"movie_details_{movie_id}"

        # Vérifier le cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data, None

        # Faire la requête API avec append_to_response pour récupérer plus de données
        data, error = self._make_request(f"movie/{movie_id}", {
            "append_to_response": "credits,videos,similar,recommendations"
        })

        if data:
            # Mettre en cache
            self.cache.set(cache_key, data)

        return data, error

    def get_movie_credits(self, movie_id: int) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """Récupère les crédits d'un film (acteurs, équipe technique)"""
        cache_key = f"movie_credits_{movie_id}"

        # Vérifier le cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data, None

        # Faire la requête API
        data, error = self._make_request(f"movie/{movie_id}/credits", {})

        if data:
            # Mettre en cache
            self.cache.set(cache_key, data)

        return data, error

# Instance globale du service
tmdb_service = TMDBService()