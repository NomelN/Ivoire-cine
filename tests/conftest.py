"""
Configuration des tests pytest
"""
import pytest
import os
from app.factory import create_app


@pytest.fixture
def app():
    """Créer une instance de l'application pour les tests"""
    # Configuration de test
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['TMDB_API_KEY'] = 'test-api-key-123'

    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })

    yield app


@pytest.fixture
def client(app):
    """Client de test pour les requêtes HTTP"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Runner pour les commandes CLI"""
    return app.test_cli_runner()


@pytest.fixture
def mock_tmdb_response():
    """Mock response pour les appels TMDB API"""
    return {
        "results": [
            {
                "id": 1,
                "title": "Film Test",
                "poster_path": "/test.jpg",
                "release_date": "2023-01-01",
                "vote_average": 8.5,
                "overview": "Un film de test"
            }
        ],
        "total_pages": 1,
        "total_results": 1
    }


@pytest.fixture
def mock_genres_response():
    """Mock response pour les genres TMDB"""
    return {
        "genres": [
            {"id": 28, "name": "Action"},
            {"id": 35, "name": "Comédie"},
            {"id": 18, "name": "Drame"}
        ]
    }