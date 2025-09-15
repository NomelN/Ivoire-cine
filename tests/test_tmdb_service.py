"""
Tests pour le service TMDB
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.tmdb_service import TMDBService, TMDBCache
import time


class TestTMDBCache:
    """Tests pour la classe TMDBCache"""

    def test_cache_set_get(self):
        """Test set et get du cache"""
        cache = TMDBCache()
        test_data = {"test": "data"}

        cache.set("test_key", test_data)
        result = cache.get("test_key")

        assert result == test_data

    def test_cache_expiry(self):
        """Test de l'expiration du cache"""
        cache = TMDBCache()
        test_data = {"test": "data"}

        # Simuler un cache expiré en modifiant le timestamp
        cache.set("test_key", test_data)
        cache._timestamps["test_key"] = time.time() - 3700  # 1h et 1min dans le passé

        result = cache.get("test_key")
        assert result is None

    def test_cache_clear(self):
        """Test du nettoyage du cache"""
        cache = TMDBCache()
        cache.set("test_key", {"test": "data"})

        cache.clear()

        assert cache.get("test_key") is None


class TestTMDBService:
    """Tests pour la classe TMDBService"""

    def setup_method(self):
        """Setup pour chaque test"""
        self.service = TMDBService()
        self.service.cache.clear()  # Nettoyer le cache entre les tests

    @patch('app.services.tmdb_service.requests.get')
    def test_make_request_success(self, mock_get):
        """Test d'une requête réussie"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        result, error = self.service._make_request("test/endpoint", {"param": "value"})

        assert error is None
        assert result == {"results": []}
        mock_get.assert_called_once()

    @patch('app.services.tmdb_service.requests.get')
    def test_make_request_timeout(self, mock_get):
        """Test d'une requête avec timeout"""
        mock_get.side_effect = Exception("Timeout")

        result, error = self.service._make_request("test/endpoint", {})

        assert result is None
        assert "Erreur inattendue" in error

    @patch('app.services.tmdb_service.requests.get')
    def test_make_request_401(self, mock_get):
        """Test d'une requête avec erreur 401"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result, error = self.service._make_request("test/endpoint", {})

        assert result is None
        assert "Clé API invalide" in error

    @patch('app.services.tmdb_service.requests.get')
    def test_make_request_404(self, mock_get):
        """Test d'une requête avec erreur 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result, error = self.service._make_request("test/endpoint", {})

        assert result is None
        assert "Ressource non trouvée" in error

    @patch.object(TMDBService, '_make_request')
    def test_get_popular_movies(self, mock_request):
        """Test de récupération des films populaires"""
        mock_data = {"results": [], "total_pages": 5}
        mock_request.return_value = (mock_data, None)

        result, error = self.service.get_popular_movies(1)

        assert error is None
        assert result["total_pages"] == 5
        mock_request.assert_called_once_with("movie/popular", {"page": 1})

    @patch.object(TMDBService, '_make_request')
    def test_get_popular_movies_with_cache(self, mock_request):
        """Test du cache pour les films populaires"""
        mock_data = {"results": [], "total_pages": 5}
        mock_request.return_value = (mock_data, None)

        # Premier appel
        result1, error1 = self.service.get_popular_movies(1)
        # Deuxième appel (doit utiliser le cache)
        result2, error2 = self.service.get_popular_movies(1)

        assert result1 == result2
        # _make_request ne doit être appelé qu'une fois grâce au cache
        assert mock_request.call_count == 1

    @patch.object(TMDBService, '_make_request')
    def test_search_movies(self, mock_request):
        """Test de recherche de films"""
        mock_data = {"results": []}
        mock_request.return_value = (mock_data, None)

        result, error = self.service.search_movies("batman", 1)

        assert error is None
        mock_request.assert_called_once_with("search/movie", {
            "query": "batman",
            "page": 1
        })

    @patch.object(TMDBService, '_make_request')
    def test_get_genres(self, mock_request):
        """Test de récupération des genres"""
        mock_data = {"genres": [{"id": 28, "name": "Action"}]}
        mock_request.return_value = (mock_data, None)

        result, error = self.service.get_genres()

        assert error is None
        assert result == mock_data
        mock_request.assert_called_once_with("genre/movie/list", {})

    @patch.object(TMDBService, '_make_request')
    def test_discover_movies_by_genre(self, mock_request):
        """Test de découverte par genre"""
        mock_data = {"results": [], "total_pages": 10}
        mock_request.return_value = (mock_data, None)

        result, error = self.service.discover_movies_by_genre(28, 2)

        assert error is None
        assert result["total_pages"] == 10
        mock_request.assert_called_once_with("discover/movie", {
            "with_genres": 28,
            "page": 2
        })

    @patch.object(TMDBService, '_make_request')
    def test_total_pages_limit(self, mock_request):
        """Test de la limitation du nombre de pages"""
        mock_data = {"results": [], "total_pages": 1000}
        mock_request.return_value = (mock_data, None)

        result, error = self.service.get_popular_movies(1)

        assert error is None
        # total_pages doit être limité à 500
        assert result["total_pages"] == 500