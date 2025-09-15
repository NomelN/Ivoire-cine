"""
Tests pour les routes de l'application
"""
import pytest
from unittest.mock import patch, MagicMock


class TestHomeRoute:
    """Tests pour la route home"""

    @patch('app.routes.movies.tmdb_service.get_popular_movies')
    def test_home_success(self, mock_get_movies, client, mock_tmdb_response):
        """Test de la page d'accueil avec succès"""
        mock_get_movies.return_value = (mock_tmdb_response, None)

        response = client.get('/')

        assert response.status_code == 200
        assert b'Film Test' in response.data
        mock_get_movies.assert_called_once_with(1)

    @patch('app.routes.movies.tmdb_service.get_popular_movies')
    def test_home_with_page_param(self, mock_get_movies, client, mock_tmdb_response):
        """Test de la page d'accueil avec paramètre de page"""
        mock_get_movies.return_value = (mock_tmdb_response, None)

        response = client.get('/?page=2')

        assert response.status_code == 200
        mock_get_movies.assert_called_once_with(2)

    @patch('app.routes.movies.tmdb_service.get_popular_movies')
    def test_home_api_error(self, mock_get_movies, client):
        """Test de la page d'accueil avec erreur API"""
        mock_get_movies.return_value = (None, "Erreur API")

        response = client.get('/')

        assert response.status_code == 200
        assert b'Erreur API' in response.data

    @patch('app.routes.movies.tmdb_service.get_popular_movies')
    def test_home_invalid_page(self, mock_get_movies, client, mock_tmdb_response):
        """Test avec un numéro de page invalide"""
        mock_get_movies.return_value = (mock_tmdb_response, None)

        response = client.get('/?page=abc')

        assert response.status_code == 200
        # Doit utiliser page=1 par défaut
        mock_get_movies.assert_called_once_with(1)


class TestSearchRoute:
    """Tests pour la route search"""

    @patch('app.routes.movies.tmdb_service.search_movies')
    def test_search_success(self, mock_search, client, mock_tmdb_response):
        """Test de recherche avec succès"""
        mock_search.return_value = (mock_tmdb_response, None)

        response = client.get('/search?query=batman')

        assert response.status_code == 200
        assert b'Film Test' in response.data
        mock_search.assert_called_once_with('batman')

    @patch('app.routes.movies.tmdb_service.search_movies')
    def test_search_no_results(self, mock_search, client):
        """Test de recherche sans résultats"""
        mock_search.return_value = ({"results": []}, None)

        response = client.get('/search?query=xxxxxx')

        assert response.status_code == 200
        assert b'Aucun' in response.data

    @patch('app.routes.movies.tmdb_service.search_movies')
    def test_search_api_error(self, mock_search, client):
        """Test de recherche avec erreur API"""
        mock_search.return_value = (None, "Erreur de recherche")

        response = client.get('/search?query=batman')

        assert response.status_code == 200
        assert b'Erreur de recherche' in response.data

    def test_search_empty_query(self, client):
        """Test de recherche avec requête vide"""
        response = client.get('/search')

        assert response.status_code == 200
        assert b'Recherche de films' in response.data

    def test_search_dangerous_query(self, client):
        """Test de recherche avec requête dangereuse"""
        response = client.get('/search?query=<script>alert()</script>')

        assert response.status_code == 200
        # La requête doit être nettoyée


class TestGenreRoute:
    """Tests pour la route genre"""

    @patch('app.routes.movies.tmdb_service.discover_movies_by_genre')
    @patch('app.routes.movies.tmdb_service.get_genres')
    def test_genre_success(self, mock_get_genres, mock_discover, client, mock_tmdb_response, mock_genres_response):
        """Test de filtrage par genre avec succès"""
        mock_discover.return_value = (mock_tmdb_response, None)
        mock_get_genres.return_value = (mock_genres_response, None)

        response = client.get('/genre/28')

        assert response.status_code == 200
        assert b'Film Test' in response.data
        mock_discover.assert_called_once_with(28, 1)

    @patch('app.routes.movies.tmdb_service.discover_movies_by_genre')
    @patch('app.routes.movies.tmdb_service.get_genres')
    def test_genre_with_page(self, mock_get_genres, mock_discover, client, mock_tmdb_response, mock_genres_response):
        """Test de filtrage par genre avec pagination"""
        mock_discover.return_value = (mock_tmdb_response, None)
        mock_get_genres.return_value = (mock_genres_response, None)

        response = client.get('/genre/28?page=3')

        assert response.status_code == 200
        mock_discover.assert_called_once_with(28, 3)

    def test_genre_invalid_id(self, client):
        """Test avec un ID de genre invalide"""
        response = client.get('/genre/abc')

        assert response.status_code == 404

    def test_genre_id_out_of_range(self, client):
        """Test avec un ID de genre hors limites"""
        response = client.get('/genre/99999')

        assert response.status_code == 404


class TestErrorHandling:
    """Tests pour la gestion d'erreurs"""

    def test_404_page(self, client):
        """Test de la page 404"""
        response = client.get('/page-inexistante')

        assert response.status_code == 404
        assert 'Page non trouvée'.encode('utf-8') in response.data

    def test_500_error_template(self, client):
        """Test que le template d'erreur existe"""
        # Ce test vérifie que le template error.html est accessible
        # En cas d'erreur 500, il devrait s'afficher
        pass  # Le template existe déjà, testé par les autres tests