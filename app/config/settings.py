"""
Configuration de l'application Ivoire Ciné
"""
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

class Config:
    """Configuration de base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Configuration TMDB API
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

    # Configuration des requêtes
    REQUEST_TIMEOUT = 10  # secondes
    MAX_PAGE_LIMIT = 1000
    MAX_QUERY_LENGTH = 100
    MAX_GENRE_ID = 10779  # Limite TMDB

    # Cache configuration
    CACHE_TIMEOUT = 3600  # 1 heure en secondes

    @classmethod
    def validate(cls):
        """Valide la configuration au démarrage"""
        if not cls.TMDB_API_KEY or cls.TMDB_API_KEY == "your_api_key_here":
            raise ValueError(
                "TMDB_API_KEY manquante ou invalide. "
                "Vérifiez votre fichier .env et consultez .env.example"
            )

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    FLASK_ENV = 'production'
    # En production, utiliser une vraie clé secrète
    SECRET_KEY = os.getenv('SECRET_KEY')

    @classmethod
    def validate(cls):
        super().validate()
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY de production requise")

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    DEBUG = True
    # Utiliser une clé API de test si disponible
    TMDB_API_KEY = os.getenv('TMDB_TEST_API_KEY', os.getenv('TMDB_API_KEY'))

# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env_name=None):
    """Retourne la configuration pour l'environnement spécifié"""
    env_name = env_name or os.getenv('FLASK_ENV', 'default')
    return config.get(env_name, config['default'])